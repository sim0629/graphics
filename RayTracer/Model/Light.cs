using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Media;
using System.Windows.Media.Media3D;

namespace Gyumin.Graphics.RayTracer.Model
{
    using MathUtil;

    public abstract class Light
    {
        protected Color color;

        public Color Ambient { get; protected set; }

        public abstract Color IntensityAt(Point3D point);

        public abstract Ray RayFrom(Point3D point);
    }
}
