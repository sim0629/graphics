using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Media;

namespace Gyumin.Graphics.RayTracer.Material
{
    public class Phong
    {
        public Color Ambient { get; private set; }

        public Color Diffuse { get; private set; }

        public Color Specular { get; private set; }

        public double Shininess { get; private set; }

        public double K_Reflection { get; private set; }

        public double K_Refraction { get; private set; }

        public double N_Index { get; private set; }

        public Phong(Color ambient, Color diffuse, Color specular, double shininess,
            double k_reflection, double k_refraction, double n_index)
        {
            this.Ambient = ambient;
            this.Diffuse = diffuse;
            this.Specular = specular;
            this.Shininess = shininess;
            this.K_Reflection = k_reflection;
            this.K_Refraction = k_refraction;
            this.N_Index = n_index;
        }
    }
}
