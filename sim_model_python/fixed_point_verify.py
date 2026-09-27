import os

import numpy as np


def run_bit_growth_test():
    print("--- Running SDR Fixed-Point Bit-Growth Analysis ---")

    # Generate an ideal floating-point signal.
    t = np.linspace(0, 1, 1000, endpoint=False)
    floating_signal = 0.7 * np.sin(2 * np.pi * 5 * t)

    # Quantize to signed 16-bit fixed-point values with 15 fractional bits.
    fractional_bits = 15
    scaling_factor = 2**fractional_bits
    quantized_signal = np.round(floating_signal * scaling_factor).astype(np.int32)
    quantized_signal = np.clip(quantized_signal, -32768, 32767)

    # Multiply by a fixed-point local oscillator; the product has bit growth.
    local_oscillator_val = int(0.8 * scaling_factor)
    mixed_signal_32bit = quantized_signal * local_oscillator_val

    # Remove the fractional product bits and saturate to signed 16-bit range.
    truncated_signal_16bit = np.right_shift(mixed_signal_32bit, fractional_bits)
    truncated_signal_16bit = np.clip(
        truncated_signal_16bit, -32768, 32767
    ).astype(np.int16)

    # Compare the fixed-point output with the original floating-point signal.
    reconstructed_float = truncated_signal_16bit / scaling_factor
    quantization_noise = floating_signal - reconstructed_float
    noise_variance = np.var(quantization_noise)
    sqnr = (
        10 * np.log10(np.var(floating_signal) / noise_variance)
        if noise_variance > 0
        else float("inf")
    )

    print(f"Max Input Value (Float): {np.max(floating_signal):.4f}")
    print(f"Max Input Value (16-bit Int): {np.max(quantized_signal)}")
    print(f"Max Mixed Value (32-bit Grown Int): {np.max(mixed_signal_32bit)}")
    print(f"Final Signal-to-Quantization-Noise Ratio (SQNR): {sqnr:.2f} dB")

    # Save input and expected output vectors for VHDL testbenches.
    output_dir = os.path.join("sim_model_python", "test_vectors")
    os.makedirs(output_dir, exist_ok=True)
    np.savetxt(
        os.path.join(output_dir, "input_stimulus.txt"), quantized_signal, fmt="%d"
    )
    np.savetxt(
        os.path.join(output_dir, "expected_output.txt"), truncated_signal_16bit, fmt="%d"
    )
    print("✓ Successfully saved fixed-point test vectors for VHDL testbenches.")


if __name__ == "__main__":
    run_bit_growth_test()