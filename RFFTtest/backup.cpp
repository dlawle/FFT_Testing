#include "daisy_patch_sm.h"
#include "daisysp.h"
#include "patch_bay.h"
#include "arm_math.h"
#include "arm_const_structs.h"

using namespace daisy;
using namespace patch_sm;
using namespace daisysp;

DaisyPatchSM hw;
Patch_Bay    pb;
#define TEST_LENGTH_SAMPLES 2048

FIRFilterImplGeneric<TEST_LENGTH_SAMPLES, TEST_LENGTH_SAMPLES/4> fir;

arm_rfft_fast_instance_f32 S = {
	{ 512, twiddleCoef_512, armBitRevIndexTable512, ARMBITREVINDEXTABLE_512_TABLE_LENGTH },
	1024u,
	(float32_t *)twiddleCoef_rfft_1024
};

/* -------------------------------------------------------------------
* External Input and Output buffer Declarations for FFT Bin Example
* ------------------------------------------------------------------- */
float32_t testInput[TEST_LENGTH_SAMPLES];
static float32_t testOutput[TEST_LENGTH_SAMPLES/2];

/* ------------------------------------------------------------------
* Global variables for FFT Bin Example
* ------------------------------------------------------------------- */
uint32_t fftSize = 1024;
uint32_t ifftFlag = 0;
uint32_t doBitReverse = 1;

/* Reference index at which max energy of bin ocuurs */
uint32_t refIndex = 213, testIndex = 0;

// global, so do_fft() knows when to run
int fft_buf_index = 0;
float f;

float doFft();
float doFftSpect();
void DisplayTimeWaveform();
void DisplayWaveform();

void UpdateOled(float fl)
{
    pb.display.Fill(false);
    std::string str = std::to_string(static_cast<int>(fl));
    char *cstr = &str[0];
    pb.display.SetCursor(0, 0);
    pb.display.WriteString(cstr, Font_11x18, true);

    pb.display.Update();
}

void AudioCallback(AudioHandle::InputBuffer in, AudioHandle::OutputBuffer out, size_t size)
{
	hw.ProcessAllControls();
	for (size_t i = 0; i < size; i++)
	{
		if (fft_buf_index < TEST_LENGTH_SAMPLES) 
		{
			testInput[fft_buf_index++] = IN_L[i]+IN_R[i];
			testInput[fft_buf_index++] = 0.f;
		}

		OUT_L[i] = IN_L[i];
		OUT_R[i] = IN_R[i];
	}
}

int main(void)
{
	hw.Init();
	hw.SetAudioBlockSize(4); // number of samples handled per callback
	hw.SetAudioSampleRate(SaiHandle::Config::SampleRate::SAI_48KHZ);

	pb.Init();
	hw.StartAudio(AudioCallback);
	while(1) 
	{
		if (fft_buf_index >= TEST_LENGTH_SAMPLES)
		{
			// test one: call function and return "frequency"
			//f = doFft();

			// test two: call function and return "magnitude"
			f = doFftSpect();

			fft_buf_index = 0;
		}
		hw.Delay(20);
		DisplayWaveform();
	}
}


float doFft()
{
	float32_t maxValue;
	uint32_t Nbins = TEST_LENGTH_SAMPLES / 2;
	int Fmax = hw.AudioSampleRate();
	/* Process the data through the CFFT/CIFFT module */
	arm_rfft_fast_f32(&S, testInput, testOutput, 0);

	/* Process the data through the Complex Magnitude Module for
	calculating the magnitude at each bin */	
	arm_cmplx_mag_f32(testInput, testOutput, fftSize);

	/* Calculates maxValue and returns corresponding BIN value */
	arm_max_f32(testOutput, fftSize, &maxValue, &testIndex);

	/*
	to calculate the freq of the selected bin
    N (Bins) = FFT Size/2
	Frequency = BinIndex * SamplingFrequency / FFTSize
	*/

	// error test
	if (testIndex >= Nbins)	
		return -1.f;

	return static_cast<float>(testIndex) * static_cast<float>(Fmax) / static_cast<float>(fftSize);
	//return (float) testIndex * ((float)Fmax / Nbins);
}


float doFftSpect()
{
	float32_t maxValue;
	/* Process the data through the CFFT/CIFFT module */
	arm_rfft_fast_f32(&S, testInput, testOutput, ifftFlag);

	/* Process the data through the Complex Magnitude Module for
	calculating the magnitude at each bin */	
	arm_cmplx_mag_f32(testInput, testOutput, fftSize);

    /* Find the maximum magnitude in the spectrum */
    arm_max_f32(testOutput, fftSize / 2, &maxValue, &testIndex);

    return maxValue;
}

void DisplayTimeWaveform()
{
    // Clear the display
    pb.display.Fill(false);

    // Draw waveform using non-zero audioBuffer values
    int x = 0; // Initialize x-coordinate
    for (int i = 0; i < fft_buf_index; i += 2)
    {
        // Calculate y-coordinate based on non-zero audio amplitude
        float amplitude = testInput[i];
        if (amplitude != 0.0) // Skip zero values
        {
            int y = static_cast<int>((amplitude + 1.0) * 0.5 * (pb.display.Height() - 1));

            // Draw a vertical line at the current position
            pb.display.DrawPixel(x++, pb.display.Height() - y, true);
        }
    }

    // Update the display
    pb.display.Update();
}

void DisplayWaveform()
{
    // Apply FFT to audio data
    arm_rfft_fast_f32(&S, testInput, testOutput, ifftFlag);
   	arm_cmplx_mag_f32(testInput, testOutput, fftSize);

    // Clear the display
    pb.display.Fill(false);

    // Draw waveform using testOutput
    for (int x = 0; x < pb.display.Width(); x++)
    {
        int y = static_cast<int>(testOutput[x] * pb.display.Height());
        pb.display.DrawPixel(x, pb.display.Height() - y, true);
    }

    // Update the display
    pb.display.Update();
}