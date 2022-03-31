import java.util.*;

public class Vault2 {
    public static void main(String args[]) {
        Vault2 vaultDoor = new Vault2();
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
        String password = "TGCV)RIGL$ACCJ";
        for(int i=0;i<input.length();i++){
            input = input.substring(0,i) + (char)(input.charAt(i)-i) + input.substring(i+1); //Wonder what this does?
        }
        return input.equals(password);
    }
    
}