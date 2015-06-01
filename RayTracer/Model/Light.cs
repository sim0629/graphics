using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Media.Media3D;

namespace Gyumin.Graphics.RayTracer.Model
{
    using Material;
    using MathUtil;

    public abstract class Light
    {
        protected FloatColor color;

        public FloatColor Ambient { get; protected set; }

        public abstract FloatColor IntensityAt(Point3D point);

        public abstract Ray RayFrom(Point3D point);

        public abstract double DistanceFrom(Point3D point);
    }
}
