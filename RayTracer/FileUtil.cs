using Microsoft.Win32;
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Media.Imaging;

namespace Gyumin.Graphics.RayTracer
{
    public static class FileUtil
    {
        public static void SaveToPng(BitmapSource src)
        {
            var dialog = new SaveFileDialog()
            {
                FileName = "image",
                DefaultExt = ".png",
                Filter = "PNG|*.png",
            };
            if (dialog.ShowDialog(App.Current.MainWindow) != true)
                return;
            using (var stream = new FileStream(dialog.FileName, FileMode.Create))
            {
                var encoder = new PngBitmapEncoder();
                encoder.Frames.Add(BitmapFrame.Create(src));
                encoder.Save(stream);
            }
        }

        public static string OpenStl()
        {
            var dialog = new OpenFileDialog()
            {
                Filter = "ASCII STL|*.stl",
            };
            if (dialog.ShowDialog(App.Current.MainWindow) != true)
                return null;
            return dialog.FileName;
        }
    }
}
