import java.awt.*;

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
        switch (direct) {
            case 0 -> Main.object.next_frame(-1);
            case 1 -> Main.object.next_frame(1);
            case 2 -> Main.object.next_frame(-6);
            case 3 -> Main.object.next_frame(6);
        }
    }


    public void paint(Graphics2D g) {
        g.setRenderingHint(RenderingHints.KEY_INTERPOLATION, RenderingHints.VALUE_INTERPOLATION_NEAREST_NEIGHBOR);
        g.drawImage(Main.object.current_image, 0, 0, Main.board_width, Main.board_height, null);
        g.setRenderingHint(RenderingHints.KEY_TEXT_ANTIALIASING, RenderingHints.VALUE_TEXT_ANTIALIAS_ON);
        if (Main.object.is_select()) {
            g.setColor(Color.red);
            g.setFont(new Font("Courier", Font.PLAIN, 18));
            g.drawString("Saved", 12, 24);
        }

        g.setColor(Color.yellow);
        g.setFont(new Font("Courier", Font.PLAIN, 12));
        g.drawString(Main.object.show_name(), Main.board_width - 165, Main.board_height - 8);

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

    public void save() {
        Main.object.do_select();
    }

    public void delete() {
        Main.object.do_cancel();
    }

    public void page_down() {
        Main.object.next_frame(50);
    }

    public void page_up() {
        Main.object.next_frame(-50);
    }
}
