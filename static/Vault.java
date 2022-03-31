import java.util.*;

public class Vault {
    public static void main(String args[]) {
        Vault vaultDoor = new Vault();
        Scanner scanner = new Scanner(System.in);
        System.out.print("Enter vault password: ");
        String userInput = scanner.next(); //Input of the form FLAG{..}
        String input = userInput.substring("FLAG{".length(),userInput.length()-1); //Consider the part within curly braces
        if (vaultDoor.checkPassword(input)) {
            System.out.println("Access granted.");
        }
        else {
            System.out.println("Access denied!");
        }
        scanner.close();
    }

    boolean checkPassword(String input){
        String password = "5ma3-an4grt-s1mpl5uj";
        char[] buffer = new char[20];
        
        for(int i=0;i<3;i++) buffer[i]=input.charAt(19-i);
        for(int i=3;i<10;i++) buffer[i]=input.charAt(i+7);
        for(int i=10;i<17;i++) buffer[i]=input.charAt(i-7);
        for(int i=17;i<20;i++) buffer[i]=input.charAt(19-i);
        //Wonder what this does?

        return (new String(buffer)).equals(password);
    }
    
}