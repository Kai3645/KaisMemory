import java.awt.event.KeyAdapter;
import java.awt.event.KeyEvent;

class Keyboard extends KeyAdapter {
	public void keyPressed(KeyEvent e) {
		int key = e.getKeyCode();
		switch (key) {
			case KeyEvent.VK_BACK_SPACE: {
				Main.action.del_point();
				break;
			}
			case KeyEvent.VK_ESCAPE: {
				Main.action.finish_flag = true;
				break;
			}
			case KeyEvent.VK_UP: {
				Main.action.frame_up();
				break;
			}
			case KeyEvent.VK_DOWN: {
				Main.action.frame_down();
				break;
			}
			case KeyEvent.VK_LEFT: {
				Main.action.frame_left();
				break;
			}
			case KeyEvent.VK_RIGHT: {
				Main.action.frame_right();
				break;
			}
			case KeyEvent.VK_S: {
				Main.process_save();
				break;
			}
			case KeyEvent.VK_L: {
				Main.process_load();
				break;
			}
			case KeyEvent.VK_Q: {
				Main.process_clean();
				break;
			}
			case KeyEvent.VK_C: {
				Main.action.frame_clean();
				break;
			}
			default: {
				System.out.println(">> unknown key .. ");
			}
		}
	}

	public void keyReleased(KeyEvent e) {

	}

	public void keyTyped(KeyEvent e) {

	}

}
