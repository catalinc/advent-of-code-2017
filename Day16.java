import java.io.IOException;
import java.nio.charset.Charset;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Paths;

class Move {
  final char type;
  final int start;
  final int end;

  Move(char type, int start, int end) {
    this.type = type;
    this.start = start;
    this.end = end;
  }
}

class Dance {
  final Move[] moves;
  private int current = 0;

  private Dance(int size) {
    this.moves = new Move[size];
  }

  private void add(Move move) {
    this.moves[current] = move;
    current++;
  }

  static Dance parse(String str) {
    String[] tokens = str.split(",");
    Dance dance = new Dance(tokens.length);
    int start, end, slash;
    for (int i = 0; i < tokens.length; i++) {
      String token = tokens[i];
      switch (token.charAt(0)) {
        case 's':
          start = Integer.parseInt(token.substring(1));
          dance.add(new Move('s', start, 0));
          break;
        case 'x':
          slash = token.indexOf('/');
          start = Integer.parseInt(token.substring(1, slash));
          end = Integer.parseInt(token.substring(slash + 1));
          dance.add(new Move('x', start, end));
          break;
        case 'p':
          start = token.charAt(1);
          end = token.charAt(3);
          dance.add(new Move('p', start, end));
      }
    }
    return dance;
  }
}

class ProgramGroup {
  private static final String ALPHABET = "abcdefghijklmnopqrstuvwxyz";
  private char[] programs;
  private char[] buffer;

  ProgramGroup(int size) {
    this.programs = new char[size];
    for (int i = 0; i < size; i++) {
      programs[i] = ALPHABET.charAt(i);
    }
    this.buffer = new char[size];
  }

  void dance(Dance dance) {
    int src, dst;
    char ch1, ch2, t;
    char[] tmp;
    for (int i = 0; i < dance.moves.length; i++) {
      Move m = dance.moves[i];
      switch (m.type) {
        case 's':
          src = m.start;
          dst = 0;
          for (int j = programs.length - src; j < programs.length; j++) {
            buffer[dst++] = programs[j];
          }
          for (int j = 0; j < programs.length - src; j++) {
            buffer[dst++] = programs[j];
          }
          tmp = programs;
          programs = buffer;
          buffer = tmp;
          break;
        case 'x':
          src = m.start;
          dst = m.end;
          t = programs[src];
          programs[src] = programs[dst];
          programs[dst] = t;
          break;
        case 'p':
          src = 0;
          dst = 0;
          ch1 = (char) m.start;
          ch2 = (char) m.end;
          for (int j = 0; j < programs.length; j++) {
            if (programs[j] == ch1) {
              src = j;
              break;
            }
          }
          for (int j = 0; j < programs.length; j++) {
            if (programs[j] == ch2) {
              dst = j;
              break;
            }
          }
          t = programs[src];
          programs[src] = programs[dst];
          programs[dst] = t;
          break;
      }
    }
  }

  @Override
  public String toString() {
    StringBuilder sb = new StringBuilder();
    for (int i = 0; i < programs.length; i++) {
      sb.append(programs[i]);
    }
    return sb.toString();
  }
}

public class Day16 {
  private static String readFile(String path, Charset encoding)
          throws IOException {
    byte[] encoded = Files.readAllBytes(Paths.get(path));
    return new String(encoded, encoding);
  }

  public static void main(String[] args) throws IOException {
    if (args.length == 2) {
      final String filename = args[0];
      final int repeat = Integer.parseInt(args[1]);
      final String content = readFile(filename, StandardCharsets.UTF_8);
      final Dance dance = Dance.parse(content);
      final ProgramGroup pg = new ProgramGroup(16);
      pg.dance(dance);
      long threshold = 1_000_000;
      for (int i = 0; i < repeat; i++) {
        pg.dance(dance);
        if (i >= threshold) {
          System.out.println(i);
          threshold *= 10;
        }
      }
      System.out.println(pg);
    } else {
      long start = System.nanoTime();
      Dance dance = Dance.parse("s1,x3/4,pe/b");
      ProgramGroup pg = new ProgramGroup(5);
      pg.dance(dance);
      long elapsed = System.nanoTime() - start;
      System.out.println(pg + " in " + ((double)elapsed / 1000000)+ " ms");
    }
  }
}