import java.awt.*;
import java.awt.image.BufferedImage;

class Action {
    int[] mouse_pos = new int[2];

    public Action() {

    }

    public void update() {
        Main.object.update();
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
        Main.object.draw(g);
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
