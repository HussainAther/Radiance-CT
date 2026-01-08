import unittest
import numpy as np
from src.rbyrct.projector import RBYRCTProjector

class TestPhysicsEngine(unittest.TestCase):
    def setUp(self):
        # Create a simple 10x10x10 volume of water (mu = 0.19 at 20keV)
        self.volume = np.ones((10, 10, 10)) * 0.19
        self.projector = RBYRCTProjector(volume_dims=(10,10,10), voxel_size=1.0)

    def test_beer_lambert_math(self):
        """
        Verify I = I0 * exp(-mu * d)
        For d=10, mu=0.19, I0=1000: I should be ~149.5
        """
        source = np.array([-5, 5, 5])
        pixel = np.array([15, 5, 5])
        
        calculated_intensity = self.projector.forward_project_ray(source, pixel, self.volume)
        expected_intensity = 1000 * np.exp(-0.19 * 10)
        
        self.assertAlmostEqual(calculated_intensity, expected_intensity, places=2)
        print("✅ Physics Test Passed: Beer-Lambert calculation is accurate.")

if __name__ == '__main__':
    unittest.main()
