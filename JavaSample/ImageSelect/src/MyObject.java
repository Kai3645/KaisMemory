import javax.imageio.ImageIO;
import java.awt.*;
import java.io.File;
import java.io.IOException;
import java.util.Arrays;

public class MyObject {
    private static final String main_folder = "/home/kai/PycharmProjects/pyCenter/diary_output/d_20201029";
    private static final String folder_out = "/home/kai/PycharmProjects/pyCenter/diary_output/d_20201030";
    private static final int folder_total = 13;

    String[] name_list;
    String current_folder;
    Image current_img;
    String new_name;

    int folder_idx, name_idx;

    boolean saved_flag = false;

    public boolean read_image(int dx) {
        for (; name_idx < name_list.length && name_idx >= 0; name_idx += dx) {
            if (name_list[name_idx].charAt(0) == '.') continue;
            if (!name_list[name_idx].contains(".jpg")) continue;

//            System.out.println(">> read image \"" + name_list[name_idx] + "\"");

            try {
                String path = current_folder + "/" + name_list[name_idx];
                current_img = ImageIO.read(new File(path));
                new_name = String.format("v_%03d_", folder_idx) + name_list[name_idx];
                saved_flag = new File(folder_out + "/" + new_name).exists();
            } catch (IOException e) {
                e.printStackTrace();
            }
            return true;
        }
        return false;
    }

    public boolean set_folder(int dx) {
        int df = dx > 0 ? 1 : -1;
        for (; folder_idx < folder_total && folder_idx >= 0; folder_idx += df) {
            current_folder = main_folder + String.format("/v_%03d", folder_idx);

            System.out.printf(">> folder @ \"v_%03d\"\n", folder_idx);

            File f = new File(current_folder);
            name_list = f.list();

            if (name_list == null) continue;
            Arrays.sort(name_list);
            name_idx = dx > 0 ? 0 : name_list.length - 1;
            if (read_image(dx)) return true;
        }
        return false;
    }

    public void next_image(int dx) {
        int save_name_idx = name_idx;
        int save_folder_idx = folder_idx;

        name_idx += dx;
        if (read_image(dx)) return;
        folder_idx += dx > 0 ? 1 : -1;
        if (set_folder(dx)) return;
        name_idx = save_name_idx;
        folder_idx = save_folder_idx;
        System.out.println(">> endle .. ");
    }

    public MyObject() {
        System.out.println(">> initiating .. ");
        folder_idx = 0;
        name_idx = 0;
        if (!set_folder(1)) System.exit(-1);

        System.out.println(">> initiated");
    }

    public void save() {
        if (saved_flag) return;
        try {
            String path1 = current_folder + "/" + name_list[name_idx];
            System.out.println(">> save " + new_name);
            String path2 = folder_out + "/" + new_name;
            String command = "cp " + path1 + " " + path2;
            Runtime.getRuntime().exec(command);
            saved_flag = true;
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public void delete() {
        if (!saved_flag) return;
        try {
            String command = "rm -f " + folder_out + "/" + new_name;
            Runtime.getRuntime().exec(command);
            saved_flag = false;
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

}
