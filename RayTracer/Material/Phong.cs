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

        public Phong(Color ambient, Color diffuse, Color specular, double shininess)
        {
            this.Ambient = ambient;
            this.Diffuse = diffuse;
            this.Specular = specular;
            this.Shininess = shininess;
        }
    }
}
