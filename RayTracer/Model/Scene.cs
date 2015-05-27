using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Media.Media3D;

namespace Gyumin.Graphics.RayTracer.Model
{
    using Material;
    using MathUtil;

    public class Scene
    {
        private Color backgroundColor = Colors.Black;

        private Light light = new Light(new Point3D(0, 1, -1));

        private Rectangle floor = new Rectangle(
            new Point3D(1, -1, 1),
            new Point3D(1, -1, -1),
            new Point3D(-1, -1, -1),
            new Point3D(-1, -1, 1),
            new Phong(Colors.Black, Colors.White, Colors.White, 1));

        private Camera camera = new Camera();

        public Scene()
        {
        }

        private Color Trace(Ray ray)
        {
            var intersection = new Point3D();
            if (Geometry.Intersects(ray, floor.Polygon, out intersection))
            {
                return floor.Material.Diffuse;
            }
            else
            {
                return this.backgroundColor;
            }
        }

        private Color Trace(double x, double y)
        {
            var ray = this.camera.GetRayToScreen(x, y);
            return this.Trace(ray);
        }

        public BitmapSource Render(int width, int height)
        {
            var pixels = new byte[3 * width * height];
            for (var i = 0; i < height; i++)
            {
                for (var j = 0; j < width; j++) {
                    var color = this.Trace(
                        (double)(2 * j + 1 - width) / width,
                        (double)(height - 2 * i + 1) / height);
                    var index = 3 * (i * width + j);
                    pixels[index + 0] = color.R;
                    pixels[index + 1] = color.G;
                    pixels[index + 2] = color.B;
                }
            }
            return BitmapSource.Create(width, height, 96, 96, PixelFormats.Rgb24, null, pixels, 3 * width);
        }
    }
}
