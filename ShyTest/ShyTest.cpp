#include "daisy_patch_sm.h"
#include "daisysp.h"
#include "patch_bay.h"
#include "shy_fft.h"
#include "stmtemp.h"
#include <algorithm>
#include "fft_handler.h"

using namespace daisy;
using namespace patch_sm;
using namespace daisysp;

#define SAMPLE_BUFFER_LENGTH 1024

DaisyPatchSM 	hw;
Patch_Bay		pb;
ShyFFT<float, SAMPLE_BUFFER_LENGTH, RotationPhasor> fft;

/* -------------------------------------------------------------------
* External Input and Output buffer Declarations for FFT Bin Example
* ------------------------------------------------------------------- */
static float fftInput[SAMPLE_BUFFER_LENGTH];
static float fftOutput[SAMPLE_BUFFER_LENGTH];
static float ifftOutput[SAMPLE_BUFFER_LENGTH];

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
    ps_amt = fmap(hw.GetAdcValue(CV_1), 0.1f, 1.0f);
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
    fft.Init();

	hw.SetAudioSampleRate(SaiHandle::Config::SampleRate::SAI_48KHZ);
	hw.StartAudio(AudioCallback);
	while(1)
	{
		Buffers();
	}
}

void fft_proc()
{
    fft.Direct(fftInput,fftOutput);
    fft.Inverse(fftOutput,ifftOutput);
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
