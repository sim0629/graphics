using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Media.Media3D;

namespace Gyumin.Graphics.RayTracer.Model
{
    using Material;
    using MathUtil;

    public class Mesh : Renderable
    {
        private List<Polygon> faces = new List<Polygon>();

        public Mesh(Phong material, string stl_file, Point3D center, double size)
        {
            this.Material = material;

            var x_min = double.MaxValue; var y_min = double.MaxValue; var z_min = double.MaxValue;
            var x_max = double.MinValue; var y_max = double.MinValue; var z_max = double.MinValue;
            var polygons = new List<List<Point3D>>();
            using (var reader = new StreamReader(stl_file, Encoding.UTF8))
            {
                var points = new List<Point3D>();
                while (!reader.EndOfStream)
                {
                    var line = reader.ReadLine().Trim().ToLower();
                    if (line.Length == 0)
                        continue;
                    if (line == "outer loop")
                    {
                        points = new List<Point3D>();
                    }
                    else if (line.StartsWith("vertex"))
                    {
                        var tokens = line.Split();
                        Debug.Assert(tokens.Length >= 4);
                        var x = double.Parse(tokens[1]);
                        var y = double.Parse(tokens[2]);
                        var z = double.Parse(tokens[3]);
                        x_min = Math.Min(x_min, x); y_min = Math.Min(y_min, y); z_min = Math.Min(z_min, z);
                        x_max = Math.Max(x_max, x); y_max = Math.Max(y_max, y); z_max = Math.Max(z_max, z);
                        points.Add(new Point3D(x, y, z));
                    }
                    else if (line == "endloop")
                    {
                        polygons.Add(points);
                    }
                }
            }
            var original_center = new Point3D((x_min + x_max) / 2, (y_min + y_max) / 2, (z_min + z_max) / 2);
            var original_size = Math.Max(Math.Max(x_max - x_min, y_max - y_min), z_max - z_min);
            foreach (var points in polygons)
            {
                var new_points = points.Select(point => center + (point - original_center) * size / original_size);
                this.faces.Add(new Polygon(new_points.ToArray()));
            }
        }

        public override bool Intersects(Ray ray, out Point3D intersection)
        {
            intersection = new Point3D();
            var min_distance2 = double.PositiveInfinity;
            foreach (var face in this.faces)
            {
                var p = new Point3D();
                if (Geometry.Intersects(ray, face, out p))
                {
                    var distance2 = (p - ray.Position).LengthSquared;
                    if (distance2 < min_distance2)
                    {
                        min_distance2 = distance2;
                        intersection = p;
                    }
                }
            }
            return !double.IsPositiveInfinity(min_distance2);
        }

        public override Vector3D NormalAt(Point3D point)
        {
            foreach (var face in this.faces)
            {
                if (Geometry.Contains(face.Plane, point))
                    return face.Plane.Normal;
            }
            return new Vector3D();
        }
    }
}
