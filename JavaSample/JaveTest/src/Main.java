import java.awt.image.BufferedImage;

public class Main {

    public static void main(String[] args) {
        for (int i = 0; i < 20; i++) {
            int x = i - 8;
            System.out.print(x + "  ");
            System.out.print(((x + 8) % 8) + "  ");


            int y = (int) (4 - Math.abs((x + 8) % 8 - 3.5f));
            System.out.print(" -> " + y + "\n");
        }
    }
}
