import math
import random

def clamp(value, clamp_value):
    return max(-clamp_value, min(clamp_value, value))

class ScreenShakeGroupStrategy():
    def strongest_impulse(impulses):
        if not impulses:
            return 0
        return max(
            (
                impulse.intensity *
                impulse.length_remaining
            )
            for impulse in impulses
        )
    current_strategy = strongest_impulse

class ScreenShakeImpulseStrategy():
    def generate_uniform_offset(elapsed_time, intensity):
        # Elapsed time tracks current shake duration until 0 (reset)
        # This allows the shake to smoothly animate over multiple impulses
        offset_x = math.sin(elapsed_time * 10) * intensity
        offset_y = math.cos(elapsed_time * 10) * intensity
        return (offset_x, offset_y)
    
    def generate_jitter_offset(intensity):
        offset_x = random.uniform(-intensity, intensity)
        offset_y = random.uniform(-intensity, intensity)
        return (offset_x, offset_y)

    def generate_offset(
            elapsed_time, 
            intensity, 
            offset_mod, 
            offset_max
        ):
        uniform_offset = (
            ScreenShakeImpulseStrategy.
            generate_uniform_offset(
                elapsed_time,
                intensity
            )
        )
        jitter_offset = (
            ScreenShakeImpulseStrategy.
            generate_jitter_offset(
                intensity
            )
        )
        # Apply any configured adjustment modifiers to offsets
        modified_uniform_x = uniform_offset[0] * offset_mod['uniform_x_mod']
        modified_uniform_y = uniform_offset[1] * offset_mod['uniform_y_mod']
        modified_jitter_x = jitter_offset[0] * offset_mod['jitter_x_mod']
        modified_jitter_y = jitter_offset[1] * offset_mod['jitter_y_mod']

        # Combine the uniform circular screenshake with jittery screen shake
        combined_x = modified_uniform_x + modified_jitter_x
        combined_y = modified_uniform_y + modified_jitter_y 

        # Limit screen shake offset by configured offset max for each axis
        final_x = clamp(combined_x, offset_max['x'])
        final_y = clamp(combined_y, offset_max['y'])
        return (final_x, final_y)
    
    current_strategy = generate_offset