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

    public class DirectionalLight : Light
    {
        private Vector3D direction;

        public DirectionalLight(Vector3D direction, Color color, Color ambient)
        {
            this.direction = direction;
            this.color = color;
            this.Ambient = ambient;
        }

        public override Color IntensityAt(Point3D point)
        {
            return this.color;
        }

        public override Ray RayFrom(Point3D point)
        {
            return new Ray(point, -this.direction);
        }
    }
}
