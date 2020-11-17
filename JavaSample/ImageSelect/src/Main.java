import javax.swing.*;
import java.awt.*;
import java.awt.image.BufferedImage;

public class Main extends JFrame {
    static final int board_width = 1280;
    static final int board_height = 720;
    static final int board_edge = 20;

    static final int global_width = board_width + 2 * board_edge;
    static final int global_height = board_height + 2 * board_edge;

    static MyJPanel panel = new MyJPanel();

    static Action action = new Action();
    static MyObject object = new MyObject();

    private Main() {
        String os_name = System.getProperty("os.name");
        System.out.println(">> User OS = \"" + os_name + "\"");
        int size_offset_w, size_offset_h;
        switch (os_name) {
            case "Linux" -> {
                size_offset_w = 0;
                size_offset_h = 37;
            }
            case "MacOS" -> {
                size_offset_w = 0;
                size_offset_h = 22;
            }
            default -> {
                size_offset_w = 10;
                size_offset_h = 10;
            }
        }

        setLocation(100, 50);
        setSize(global_width + size_offset_w,
                global_height + size_offset_h);
        setTitle("Image Selector");
        setDefaultCloseOperation(EXIT_ON_CLOSE);

        panel.setBackground(Color.black);

        BufferedImage cursorImg = new BufferedImage(1, 1, BufferedImage.TYPE_INT_ARGB);
        Cursor blankCursor = Toolkit.getDefaultToolkit().createCustomCursor(
                cursorImg, new Point(0, 0), "blank cursor");
        setCursor(blankCursor);

        Mouse mouse = new Mouse();
        panel.addMouseListener(mouse);
        panel.addMouseMotionListener(mouse);

        addKeyListener(new Keyboard());

        getContentPane().add(panel);

        setVisible(true);
        setResizable(false);
    }


    public static void main(String[] args) {
        new Main();
    }

}
