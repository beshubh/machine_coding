use std::collections::{HashSet, VecDeque};

/// Returns the minimum number of monster cells entered on a path from S to E,
/// or -1 if E is unreachable.
pub fn minimum_monster_cost(grid: &[&str]) -> i32 {
    if grid.is_empty() || grid[0].is_empty() {
        return -1;
    }
    let rows = grid.len();
    let cols = grid[0].len();
    let mut start = None;
    for (r, row) in grid.iter().enumerate() {
        for (c, &cell) in row.as_bytes().iter().enumerate() {
            if cell == b'S' {
                start = Some((r, c));
            }
        }
    }
    let Some(start) = start else {
        return -1;
    };

    let mut dist = vec![vec![i32::MAX; cols]; rows];
    let mut deque = VecDeque::new();
    dist[start.0][start.1] = 0;
    deque.push_front(start);
    let directions = [(0, 1), (0, -1), (1, 0), (-1, 0)];
    while let Some((r, c)) = deque.pop_front() {
        let current = dist[r][c];
        for (dr, dc) in &directions {
            let nr = r as isize + dr;
            let nc = c as isize + dc;
            if nr < 0 || nc < 0 || nr >= rows as isize || nc >= cols as isize {
                continue;
            }
            let (nr, nc) = (nr as usize, nc as usize);
            let cell = grid[nr].as_bytes()[nc];
            if cell == b'#' {
                continue;
            }
            let entry_cost = if cell == b'M' { 1 } else { 0 };
            let new_cost = current + entry_cost;
            if new_cost < dist[nr][nc] {
                dist[nr][nc] = new_cost;
                // this is for heap simulation
                if entry_cost == 0 {
                    deque.push_front((nr, nc));
                } else {
                    deque.push_back((nr, nc));
                }
            }
        }
    }

    for r in 0..rows {
        for c in 0..cols {
            if grid[r].as_bytes()[c] == b'E' {
                return if dist[r][c] == i32::MAX {
                    -1
                } else {
                    dist[r][c]
                };
            }
        }
    }
    -1
}

#[cfg(test)]
mod tests {
    use super::minimum_monster_cost as solve;

    #[test]
    fn adjacent_exit() {
        assert_eq!(solve(&["SE"]), 0);
    }

    #[test]
    fn empty_path() {
        assert_eq!(solve(&["S..", "##.", "..E"]), 0);
    }

    #[test]
    fn monsters_are_unavoidable() {
        assert_eq!(solve(&["SMME"]), 2);
    }

    #[test]
    fn longer_path_with_no_monsters_is_better() {
        assert_eq!(solve(&["SMME", "...."]), 0);
    }

    #[test]
    fn chooses_path_with_fewer_monsters() {
        assert_eq!(solve(&["SME", ".M."]), 1);
    }

    #[test]
    fn exit_is_unreachable() {
        assert_eq!(solve(&["S#E", "###", "..."]), -1);
    }
}
