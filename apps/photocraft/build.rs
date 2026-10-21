//! Windows only: embed the app icon and version info (VERSIONINFO) into `photocraft.exe`.
//!
//! On non-Windows targets this does nothing. The Nexus Windows build must embed the
//! generated Nexus icon: a resource compiler failure is always fatal rather than
//! silently creating an executable with a missing or stale icon.

fn main() {
    println!("cargo:rerun-if-changed=build.rs");
    println!("cargo:rerun-if-changed=../../assets/app-icon/photocraft.ico");
    if std::env::var("CARGO_CFG_TARGET_OS").as_deref() != Ok("windows") {
        return;
    }
    let mut res = winresource::WindowsResource::new();
    res.set_icon("../../assets/app-icon/photocraft.ico")
        .set("ProductName", "Nexus Photo Studio")
        .set("FileDescription", "Nexus Photo Studio image editor")
        .set("CompanyName", "Nexus Photo Studio Community")
        .set("LegalCopyright", "PhotoCraft contributors (MIT OR Apache-2.0); Nexus Photo Studio contributors.")
        .set("OriginalFilename", "NexusPhotoStudio.exe")
        .set("InternalName", "NexusPhotoStudio");
    if let Err(e) = res.compile() {
        panic!("Nexus Photo Studio requires a valid embedded Windows icon and version resources: {e}");
    }
}
