import javax.imageio.ImageIO;
import java.awt.image.BufferedImage;
import java.io.*;

public class MyObject {
    private static final String data_path = "/mnt/DATA_SSD/DR_sample_20201110/Calibration/detection/image_list.txt";
    private static final String select_path = "/mnt/DATA_SSD/DR_sample_20201110/Calibration/detection/select.txt";

    private int total;
    private float[] times;
    String[] paths;
    private int current_index = 0;
    private boolean[] save_flags;
    BufferedImage current_image;

    public MyObject() {
        System.out.println(">> initiating .. ");

        try {
            BufferedReader reader = new BufferedReader(new FileReader(data_path));
            while (reader.readLine() != null) total++;
            reader.close();

            times = new float[total];
            paths = new String[total];
            save_flags = new boolean[total];

            int idx = 0;
            reader = new BufferedReader(new FileReader(data_path));
            while (true) {
                String line = reader.readLine();
                if (line == null) break;
                String[] row = line.split(",");
                times[idx] = Float.parseFloat(row[0]);
                paths[idx] = row[1];
//                System.out.println(row[1]);
//                System.exit(0);
                save_flags[idx] = true;
                idx++;
            }
            reader.close();
            current_image = ImageIO.read(new File(paths[0]));

            idx = 0;
            reader = new BufferedReader(new FileReader(select_path));
            while (true) {
                String line = reader.readLine();
                if (line == null) break;
                save_flags[idx] = Boolean.parseBoolean(line);
                idx++;
            }
            reader.close();
        } catch (IOException e) {
            e.printStackTrace();
        }

        System.out.println(">> initiated");
    }

    public void save() {
        try {
            PrintStream myOut = new PrintStream(select_path);
            for (boolean flag : save_flags) {
                myOut.println(flag);
            }
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        }
    }

    public void do_select() {
        save_flags[current_index] = true;
    }

    public void do_cancel() {
        save_flags[current_index] = false;
    }

    public void next_frame(int i) {
        current_index += i;
        if (current_index < 0) current_index = 0;
        if (current_index >= total) current_index = total - 1;

        try {
            current_image = ImageIO.read(new File(paths[current_index]));
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public boolean is_select() {
        return save_flags[current_index];
    }

    public String show_name() {
        float rate = 100.0f * current_index / total;
        return String.format("%.4f (%.2f %%)", times[current_index], rate);
    }


}
