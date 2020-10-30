import java.awt.*;
import java.awt.image.BufferedImage;

class Action {
    int[] mouse_pos = new int[2];

    public Action() {

    }

    public void escape() {
        Main.panel.setVisible(false);
        Main.object.save();
        System.out.println(">> process finished .. ");
        System.exit(0);
    }

    public void direction(int direct) {

    }


    public void paint(Graphics2D g) {
        int w = Main.board_width / 3;
        int h =Main.board_height / 3;
        BufferedImage bfI = new BufferedImage(w, h, BufferedImage.TYPE_INT_RGB);

        // create random values pixel by pixel
        for (int y = 0; y < h; y++) {
            for (int x = 0; x < w; x++) {
                int c1 = (int) (Math.random() * 255);
                int c2 = (int) (Math.random() * 255);
                int c3 = (int) (Math.random() * 255);
                int p = (c1 << 16) | (c2 << 8) | c3;
                bfI.setRGB(x, y, p);
            }
        }
        g.setRenderingHint(RenderingHints.KEY_INTERPOLATION, RenderingHints.VALUE_INTERPOLATION_NEAREST_NEIGHBOR);
        g.drawImage(bfI, 0, 0, Main.board_width, Main.board_height, null);
    }

    public void mouse_moved() {
    }

    public void mouse_left() {

    }

    public void mouse_right() {

    }

    public void mouse_ex1() {

    }

    public void mouse_ex2() {

    }

}
