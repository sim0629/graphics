using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Gyumin.Graphics.RayTracer
{
    public static class Config
    {
        private const int imageWidth = 800;

        public static int ImageWidth { get { return imageWidth; } }

        public static double ImageWidthD { get { return imageWidth; } }

        private const int imageHeight = 600;

        public static int ImageHeight { get { return imageHeight; } }

        public static double ImageHeightD { get { return imageHeight; } }

        public static int NumberOfWorkers = Math.Max(Environment.ProcessorCount - 1, 1);

        public const int SoftShadowDegree = 4;

        public const int AntiAliasingDegree = 2;

        public const int MotionBlurDuration = 20;
    }
}
