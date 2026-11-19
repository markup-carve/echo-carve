//! Minimal C ABI used by the Echo language binding.

use carve::api::{self, Error, Options};
use std::panic::{catch_unwind, AssertUnwindSafe};
use std::ptr;
use std::slice;

const STATUS_OK: i32 = 0;
const STATUS_INVALID_POINTER: i32 = 1;
const STATUS_INPUT_INVALID: i32 = 2;
const STATUS_PANIC: i32 = 3;
const STATUS_ENGINE_ERROR: i32 = 4;

/// Render Carve source bytes to UTF-8 HTML.
///
/// Returns zero on success, one for invalid pointers, two for source input
/// rejected by the engine, three for a Rust panic, and four for another engine
/// error. Malformed UTF-8 source bytes are replaced, as in Carve 0.2.
/// On success, the caller owns
/// `out_data` and must release it with [`carve_html_free`].
///
/// # Safety
///
/// `input` must address `input_len` readable bytes. `out_data` and `out_len`
/// must be valid writable pointers.
#[no_mangle]
pub unsafe extern "C" fn carve_to_html(
    input: *const u8,
    input_len: usize,
    out_data: *mut *mut u8,
    out_len: *mut usize,
) -> i32 {
    if out_data.is_null() || out_len.is_null() {
        return STATUS_INVALID_POINTER;
    }

    ptr::write(out_data, ptr::null_mut());
    ptr::write(out_len, 0);

    if input.is_null() && input_len != 0 {
        return STATUS_INVALID_POINTER;
    }

    let bytes = if input_len == 0 {
        &[]
    } else {
        slice::from_raw_parts(input, input_len)
    };
    match catch_unwind(AssertUnwindSafe(|| api::render(bytes, &Options::default()))) {
        Ok(Ok(html)) if html.is_empty() => STATUS_OK,
        Ok(Ok(html)) => {
            let mut bytes = html.into_bytes().into_boxed_slice();
            ptr::write(out_data, bytes.as_mut_ptr());
            ptr::write(out_len, bytes.len());
            std::mem::forget(bytes);
            STATUS_OK
        }
        Ok(Err(Error::Input { .. })) => STATUS_INPUT_INVALID,
        Ok(Err(_)) => STATUS_ENGINE_ERROR,
        Err(_) => STATUS_PANIC,
    }
}

/// Release a buffer returned by [`carve_to_html`].
///
/// # Safety
///
/// The pointer and length must be an unchanged pair returned by
/// [`carve_to_html`], and the pair must be freed at most once.
#[no_mangle]
pub unsafe extern "C" fn carve_html_free(data: *mut u8, len: usize) {
    if data.is_null() {
        return;
    }
    drop(Box::from_raw(ptr::slice_from_raw_parts_mut(data, len)));
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn renders_and_releases_html() {
        let source = b"# Hello\n\n/italic/ and *bold*.";
        let mut data = ptr::null_mut();
        let mut len = 0;
        let status = unsafe { carve_to_html(source.as_ptr(), source.len(), &mut data, &mut len) };
        assert_eq!(status, STATUS_OK);
        let html = unsafe { std::str::from_utf8(slice::from_raw_parts(data, len)).unwrap() };
        assert_eq!(html, "<section id=\"Hello\">\n  <h1>Hello</h1>\n  <p><em>italic</em> and <strong>bold</strong>.</p>\n</section>");
        unsafe { carve_html_free(data, len) };
    }

    #[test]
    fn replaces_invalid_utf8_and_releases_html() {
        let source = [0xff];
        let mut data = ptr::null_mut();
        let mut len = 0;
        let status = unsafe { carve_to_html(source.as_ptr(), source.len(), &mut data, &mut len) };
        assert_eq!(status, STATUS_OK);
        let html = unsafe { std::str::from_utf8(slice::from_raw_parts(data, len)).unwrap() };
        assert_eq!(html, "<p>�</p>");
        unsafe { carve_html_free(data, len) };
    }

    #[test]
    fn uses_secure_html_defaults() {
        let source = b"```=html\n<script>alert(1)</script>\n```";
        let mut data = ptr::null_mut();
        let mut len = 0;
        let status = unsafe { carve_to_html(source.as_ptr(), source.len(), &mut data, &mut len) };
        assert_eq!(status, STATUS_OK);
        let html = unsafe { std::str::from_utf8(slice::from_raw_parts(data, len)).unwrap() };
        assert!(!html.contains("<script>"));
        assert!(html.contains("&lt;script&gt;"));
        unsafe { carve_html_free(data, len) };
    }

    #[test]
    fn denies_unsafe_link_schemes() {
        let source = b"[link](javascript:alert(1))";
        let mut data = ptr::null_mut();
        let mut len = 0;
        let status = unsafe { carve_to_html(source.as_ptr(), source.len(), &mut data, &mut len) };
        assert_eq!(status, STATUS_OK);
        let html = unsafe { std::str::from_utf8(slice::from_raw_parts(data, len)).unwrap() };
        assert!(!html.contains("href=\"javascript:"));
        unsafe { carve_html_free(data, len) };
    }

    #[test]
    fn rejects_a_null_nonempty_input_without_allocating() {
        let mut data = ptr::NonNull::<u8>::dangling().as_ptr();
        let mut len = 99;
        let status = unsafe { carve_to_html(ptr::null(), 1, &mut data, &mut len) };
        assert_eq!(status, STATUS_INVALID_POINTER);
        assert!(data.is_null());
        assert_eq!(len, 0);
    }

    #[test]
    fn accepts_an_empty_input() {
        let mut data = ptr::NonNull::<u8>::dangling().as_ptr();
        let mut len = 99;
        let status = unsafe { carve_to_html(ptr::null(), 0, &mut data, &mut len) };
        assert_eq!(status, STATUS_OK);
        assert!(data.is_null());
        assert_eq!(len, 0);
    }
}
