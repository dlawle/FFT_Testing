#include "daisy_patch_sm.h"
#include "daisysp.h"
#include "patch_bay.h"
#include "arm_const_structs.h"
#include "arm_math.h"

using namespace daisy;
using namespace patch_sm;
using namespace daisysp;

DaisyPatchSM 	hw;
Patch_Bay		pb;

//note i used 512 and 512 like in the struct you declared!
#define SAMPLE_BUFFER_LENGTH 1024
#define SAMPLE_BUFFER_LENGTH_HALF 512

arm_rfft_fast_instance_f32 fft = {   //note the name of the instance here
	{ 512, twiddleCoef_512, armBitRevIndexTable512, ARMBITREVINDEXTABLE_512_TABLE_LENGTH },
	1024u,
	(float32_t *)twiddleCoef_rfft_1024
};

/* -------------------------------------------------------------------
* External Input and Output buffer Declarations for FFT Bin Example
* ------------------------------------------------------------------- */
static float32_t fftInput[SAMPLE_BUFFER_LENGTH];
static float32_t fftOutput[SAMPLE_BUFFER_LENGTH];
static float32_t ifftOutput[SAMPLE_BUFFER_LENGTH];

/* ------------------------------------------------------------------
* Global variables for FFT Bin Example
* ------------------------------------------------------------------- */
// globals, so do_fft() knows when to run
int fft_buf_index = 0;
int ifft_buf_index = 0;
float ps_amt;
float output;

void fft_proc();
void Process(float input);
void Buffers();

void AudioCallback(AudioHandle::InputBuffer in, AudioHandle::OutputBuffer out, size_t size)
{
	hw.ProcessAllControls();
	ps_amt = fmap(hw.GetAdcValue(CV_1), 0.f, 10.f);
	for (size_t i = 0; i < size; i++)
	{
		Process(IN_L[i] + IN_R[i]);
		OUT_L[i] = output;
		OUT_R[i] = output;
	}
}

int main(void)
{
	hw.Init();
	hw.SetAudioBlockSize(64); // number of samples handled per callback

	pb.Init();

	hw.SetAudioSampleRate(SaiHandle::Config::SampleRate::SAI_48KHZ);
	hw.StartAudio(AudioCallback);
	while(1)
	{
		Buffers();
	}
}

void fft_proc()
{
	arm_rfft_fast_f32(&fft,fftInput, fftOutput, 0);
	arm_rfft_fast_f32(&fft,fftOutput, ifftOutput, 1);
}

void Process(float input)
{
	if (fft_buf_index < SAMPLE_BUFFER_LENGTH) 
	{
		fftInput[fft_buf_index++] = input;
	}

	if(ifft_buf_index < SAMPLE_BUFFER_LENGTH)
	{
		output = ifftOutput[ifft_buf_index++];
	}
}

void Buffers()
{
	if (fft_buf_index >= SAMPLE_BUFFER_LENGTH) 
	{ 
		fft_buf_index = 0; 
		fft_proc(); 
	}
	
	if (ifft_buf_index >= SAMPLE_BUFFER_LENGTH) 
	{ 
		ifft_buf_index = 0; 
	}
}
