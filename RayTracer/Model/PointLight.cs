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

    public class PointLight : Light
    {
        private Point3D position;

        public PointLight(Point3D position, Color color, Color ambient)
        {
            this.position = position;
            this.color = color;
            this.Ambient = ambient;
        }

        public override Color IntensityAt(Point3D point)
        {
            var v = this.position - point;
            var dd = v.LengthSquared;
            var d = v.Length;
            return Color.Multiply(this.color, (float)(5 / (5 + d + dd)));
        }

        public override Ray RayFrom(Point3D point)
        {
            return new Ray(point, this.position - point);
        }
    }
}
