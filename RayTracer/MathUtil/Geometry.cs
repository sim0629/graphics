using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Media.Media3D;

namespace Gyumin.Graphics.RayTracer.MathUtil
{
    public static class Geometry
    {
        public const double Epsilon = 1e-4;

        public static bool IsZero(double x)
        {
            return Math.Abs(x) < Epsilon;
        }

        public static bool LessOrEqual(double lhs, double rhs)
        {
            var diff = lhs - rhs;
            return IsZero(diff) || diff < 0;
        }

        public static bool GreaterOrEqual(double lhs, double rhs)
        {
            var diff = lhs - rhs;
            return IsZero(diff) || diff > 0;
        }

        public static double Apply(Plane plane, Point3D point)
        {
            return Vector3D.DotProduct(plane.Normal, (Vector3D)point) + plane.D;
        }

        public static bool Contains(Ray ray, Point3D point)
        {
            var v = point - ray.Position;
            if (IsZero(Vector3D.CrossProduct(ray.Direction, v).Length))
            {
                return Vector3D.DotProduct(ray.Direction, v) > 0;
            }
            return false;
        }

        public static bool Contains(Plane plane, Point3D point)
        {
            return IsZero(Apply(plane, point));
        }

        public static bool Contains(Polygon polygon, Point3D point)
        {
            Debug.Assert(Contains(polygon.Plane, point));

            Ray test_ray = null;

            var vs = new Vector3D[] { polygon[0] - point, polygon[1] - point, polygon[2] - point };
            for (var t = 0; t < 10; t++)
            {
                var d = (t / 2) * vs[t % 2] + vs[t % 2 + 1];
                var ray = new Ray(point, d);
                var is_good_ray = true;
                for (var i = 0; i < polygon.NumberOfPoints; i++)
                {
                    if (Contains(ray, polygon[i]))
                    {
                        is_good_ray = false;
                        break;
                    }
                }
                if (is_good_ray)
                {
                    test_ray = ray;
                    break;
                }
            }

            Debug.Assert(test_ray != null);

            var normal = Vector3D.CrossProduct(polygon.Plane.Normal, test_ray.Direction);
            var test_plane = new Plane(test_ray.Position, normal);

            var cross_count = 0;
            for(var i = 0; i < polygon.NumberOfPoints; i++)
            {
                var p0 = polygon[i];
                var p1 = polygon[(i + 1) % polygon.NumberOfPoints];
                if (Apply(test_plane, p0) * Apply(test_plane, p1) < 0)
                {
                    var ray = new Ray(p0, p1 - p0);
                    var intersection = new Point3D();
                    Intersects(ray, test_plane, out intersection);
                    if (Vector3D.DotProduct(intersection - point, test_ray.Direction) > 0)
                    {
                        cross_count++;
                    }
                }
            }

            return cross_count % 2 == 1;
        }

        public static bool Intersects(Ray ray, Plane plane, out Point3D intersection)
        {
            var bm = Vector3D.DotProduct(plane.Normal, ray.Direction);
            if (IsZero(bm))
            {
                intersection = new Point3D();
                return false;
            }
            var bj = -(plane.D + Vector3D.DotProduct(plane.Normal, (Vector3D)ray.Position));
            var t = bj / bm;
            intersection = ray.Position + t * ray.Direction;
            return t > Epsilon;
        }

        public static bool Intersects(Ray ray, Polygon polygon, out Point3D intersection)
        {
            intersection = new Point3D();
            if (Intersects(ray, polygon.Plane, out intersection))
            {
                return Contains(polygon, intersection);
            }
            return false;
        }

        public static bool Intersects(Ray ray, Sphere sphere, out Point3D intersection)
        {
            var to_center = sphere.Center - ray.Position;
            var to_foot_len = Vector3D.DotProduct(to_center, ray.Direction);
            var to_foot_len2 = to_foot_len * to_foot_len;
            var distance2 = to_center.LengthSquared - to_foot_len2;
            if (Geometry.GreaterOrEqual(distance2, sphere.Radius2))
            {
                intersection = new Point3D();
                return false;
            }
            var offset2 = sphere.Radius2 - distance2;
            if (Geometry.IsZero(offset2))
            {
                intersection = ray.Position + to_foot_len * ray.Direction;
            }
            else
            {
                var offset = Math.Sqrt(offset2);
                intersection = ray.Position + (to_foot_len - offset) * ray.Direction;
            }
            return true;
        }
    }
}
