using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Gyumin.Graphics.RayTracer.Material
{
    public class Phong
    {
        public FloatColor Ambient { get; private set; }

        public FloatColor Diffuse { get; private set; }

        public FloatColor Specular { get; private set; }

        public double Shininess { get; private set; }

        public double K_Reflection { get; private set; }

        public double K_Refraction { get; private set; }

        public double N_Index { get; private set; }

        public Phong(FloatColor ambient, FloatColor diffuse, FloatColor specular, double shininess,
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
