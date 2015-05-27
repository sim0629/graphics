using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Media;
using System.Windows.Media.Media3D;

namespace Gyumin.Graphics.RayTracer.Model
{
    public class Light
    {
        private Point3D position = new Point3D();

        private Color intensity = Colors.White;

        private Color ambient = Colors.White;

        public Light()
        {
        }

        public Light(Point3D position)
            : this()
        {
            this.position = position;
        }
    }
}
