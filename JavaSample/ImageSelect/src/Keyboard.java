import java.awt.event.KeyAdapter;
import java.awt.event.KeyEvent;

class Keyboard extends KeyAdapter {
    public void keyPressed(KeyEvent e) {
        switch (e.getKeyCode()) {
            case KeyEvent.VK_ESCAPE -> {
                System.out.println(">> key -> esc");
                Main.action.escape();
            }
            case KeyEvent.VK_UP -> Main.action.direction(0);
            case KeyEvent.VK_DOWN -> Main.action.direction(1);
            case KeyEvent.VK_LEFT -> Main.action.direction(2);
            case KeyEvent.VK_RIGHT -> Main.action.direction(3);
            case KeyEvent.VK_S -> Main.action.save();
            case KeyEvent.VK_D -> Main.action.delete();
            case KeyEvent.VK_PAGE_DOWN -> Main.action.page_down();
            case KeyEvent.VK_PAGE_UP -> Main.action.page_up();
            default -> {
                System.out.println(">> unknown key .. ");
                return;
            }
        }
        Main.panel.repaint();
    }

    public void keyReleased(KeyEvent e) {

    }

    public void keyTyped(KeyEvent e) {

    }

}
