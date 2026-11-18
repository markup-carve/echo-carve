use std::env;
use std::fs;

fn main() {
    let path = env::args().nth(1).expect("usage: benchmark <input.crv>");
    let source = fs::read_to_string(path).expect("could not read Carve input");
    let mut total = 0;
    for _ in 0..1_000 {
        total += carve2::api::render(source.as_str(), &carve2::api::Options::default())
            .expect("Carve render failed")
            .len();
    }
    println!("{total}");
}
