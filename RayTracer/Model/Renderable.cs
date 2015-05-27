using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Media;
using System.Windows.Media.Media3D;

namespace Gyumin.Graphics.RayTracer.Model
{
    using Material;
    using MathUtil;

    public abstract class Renderable
    {
        public Phong Material { get; protected set; }

        public abstract bool Intersects(Ray ray, out Point3D intersection);
    }
}
