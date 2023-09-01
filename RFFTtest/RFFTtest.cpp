#include "daisy_patch_sm.h"
#include "daisysp.h"
#include "patch_bay.h"
#include "arm_math.h"
#include "arm_const_structs.h"
#include "lut.h"

using namespace daisy;
using namespace patch_sm;
using namespace daisysp;

DaisyPatchSM hw;
Patch_Bay    pb;

#define TEST_LENGTH_SAMPLES 2048

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
static float32_t magOutput[TEST_LENGTH_SAMPLES/2];

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
int win_index = 0;
float f;

void DisplayWaveform();
void DisplayTimeWaveform();
void fftTest();

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
	float mod = hw.GetAdcValue(CV_1);

	hw.ProcessAllControls();
	for (size_t i = 0; i < size; i++)
	{
		if (fft_buf_index < TEST_LENGTH_SAMPLES) 
		{
			//float windowed_input = (IN_L[i]+IN_R[i]) * HANNING_WINDOW[win_index++];
			testInput[fft_buf_index++] = IN_L[i]+IN_R[i];
			testInput[fft_buf_index++] = 0.f;
		}
		OUT_L[i] = ((IN_L[i]+IN_R[i]) * mod);
		OUT_R[i] = ((IN_L[i]+IN_R[i]) * mod);
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
			fft_buf_index = 0;
			win_index = 0;
		}
		hw.Delay(5);
		fftTest();
	}
}

void DisplayWaveform()
{
	float32_t maxValue;
  	uint32_t index = 0;
    // Apply FFT to audio data
    arm_rfft_fast_f32(&S, testInput, testOutput, ifftFlag);
   	arm_cmplx_mag_f32(testOutput, magOutput, fftSize);
	arm_max_f32(magOutput, fftSize,&maxValue, &index);

    // Clear the display
    pb.display.Fill(false);

    // Draw waveform using testOutput
    for (int x = 0; x < pb.display.Width(); x++)
    {
        int y = static_cast<int>(magOutput[x] * pb.display.Height());
        pb.display.DrawPixel(x, pb.display.Height() - y, true);
    }

    // Update the display
    pb.display.Update();
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

void fftTest()
{
	float32_t maxValue;
  	uint32_t index = 0;
	// window the buffer
	arm_mult_f32(testInput,HANNING_WINDOW,testInput,TEST_LENGTH_SAMPLES);

    // Apply FFT to audio data
    //arm_rfft_fast_f32(&S, testInput, testOutput, ifftFlag);
   	//arm_cmplx_mag_f32(testOutput, magOutput, fftSize);

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