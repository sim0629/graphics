using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Media.Media3D;
using System.Windows.Navigation;
using System.Windows.Shapes;

namespace Gyumin.Graphics.RayTracer
{
    using Material;
    using Model;

    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {
        private Scene scene = new Scene();

        public MainWindow()
        {
            InitializeComponent();

            this.Loaded += MainWindow_Loaded;
        }

        private async void MainWindow_Loaded(object sender, RoutedEventArgs e)
        {
            this.ConstructScene();
            this.xImage.Source = await this.RenderSceneAsync(Config.ImageWidth, Config.ImageHeight, Config.NumberOfWorkers);
        }

        private void ConstructScene()
        {
            var light = new PointLight(
                new Point3D(0, 1, -1),
                Colors.White,
                Colors.White);
            scene.AddLight(light);

            var floor = new Rectangle(
                new Point3D(1, -1, 1),
                new Point3D(1, -1, -1),
                new Point3D(-1, -1, -1),
                new Point3D(-1, -1, 1),
                new Phong(Colors.Black, Colors.White, Colors.White, 1));
            scene.AddObject(floor);
        }

        private async Task<BitmapSource> RenderSceneAsync(int width, int height, int n)
        {
            var pixels = new byte[3 * width * height];
            var tasks = new List<Task>();
            for (var t = 0; t < n; t++)
            {
                var start_i = (height + n - 1) / n * t;
                var end_i = (height + n - 1) / n * (t + 1);
                var task = new Task(() =>
                {
                    for (var i = start_i; i < end_i && i < height; i++)
                    {
                        for (var j = 0; j < width; j++)
                        {
                            var color = this.scene.Trace(
                                (double)(2 * j + 1 - width) / width,
                                (double)(height - 2 * i + 1) / height);
                            var index = 3 * (i * width + j);
                            pixels[index + 0] = color.R;
                            pixels[index + 1] = color.G;
                            pixels[index + 2] = color.B;
                        }
                    }
                });
                task.Start();
                tasks.Add(task);
            }
            await Task.WhenAll(tasks);
            return BitmapSource.Create(
                Config.ImageWidth, Config.ImageHeight,
                96, 96,
                PixelFormats.Rgb24, null,
                pixels, 3 * Config.ImageWidth);
        }
    }
}
