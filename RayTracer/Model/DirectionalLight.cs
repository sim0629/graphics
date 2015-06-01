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

    public class DirectionalLight : Light
    {
        private Vector3D direction;

        public DirectionalLight(Vector3D direction, FloatColor color, FloatColor ambient)
        {
            this.direction = direction;
            this.color = color;
            this.Ambient = ambient;
        }

        public override FloatColor IntensityAt(Point3D point)
        {
            return this.color;
        }

        public override Ray RayFrom(Point3D point)
        {
            return new Ray(point, -this.direction);
        }

        public override double DistanceFrom(Point3D point)
        {
            return double.PositiveInfinity;
        }
    }
}
