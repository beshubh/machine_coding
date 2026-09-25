use std::collections::VecDeque;
use std::fs::File;
use std::io::{self, BufRead, BufReader};
use std::path::Path;

/// Returns the last `n` lines in their original order.
/// Returned strings must not contain trailing newline characters.
pub fn tail(path: &Path, n: usize) -> io::Result<Vec<String>> {
    let reader = BufReader::new(File::open(path)?);
    let mut last_lines = VecDeque::new();
    for line in reader.lines() {
        let line = line?;
        if last_lines.len() == n {
            last_lines.pop_front();
        }
        last_lines.push_back(line);
    }
    Ok(last_lines.into_iter().collect())
}

#[cfg(test)]
mod tests {
    use super::tail;
    use std::fs;
    use tempfile::NamedTempFile;

    fn run(contents: &str, n: usize) -> Vec<String> {
        let file = NamedTempFile::new().unwrap();
        fs::write(file.path(), contents).unwrap();
        tail(file.path(), n).unwrap()
    }

    #[test]
    fn returns_last_n_lines_in_original_order() {
        assert_eq!(run("one\ntwo\nthree\nfour\n", 2), ["three", "four"]);
    }

    #[test]
    fn returns_all_lines_when_n_exceeds_line_count() {
        assert_eq!(run("one\ntwo\n", 5), ["one", "two"]);
    }

    #[test]
    fn zero_returns_empty() {
        assert!(run("one\ntwo\n", 0).is_empty());
    }

    #[test]
    fn empty_file_returns_empty() {
        assert!(run("", 3).is_empty());
    }

    #[test]
    fn handles_file_without_final_newline() {
        assert_eq!(run("one\ntwo\nthree", 2), ["two", "three"]);
    }

    #[test]
    fn preserves_blank_lines() {
        assert_eq!(run("one\n\nthree\n\n", 3), ["", "three", ""]);
    }

    #[test]
    fn handles_crlf_line_endings() {
        assert_eq!(run("one\r\ntwo\r\nthree\r\n", 2), ["two", "three"]);
    }
}
