import streamlit as st
import uuid
from app_komentar_manager import login_user, login_session_is_valid, get_youtube_channels, activate_channel, get_suspicious_comments, handle_selected_comments, extract_video_id

google_logo_url = "https://upload.wikimedia.org/wikipedia/commons/c/c1/Google_%22G%22_logo.svg"
refresh = """
            <script>
                setTimeout(function(){
                    window.location.reload();
                }, 3000);  // Delay 1 detik biar user lihat dulu pesan suksesnya
            </script>
        """

def main():
    if 'chosen_channel' not in st.session_state:
        st.session_state.chosen_channel = None
    if 'youtube' not in st.session_state:
        st.session_state.youtube = None
    if 'is_owner' not in st.session_state:
        st.session_state.is_owner = False
    if 'comments' not in st.session_state:
        st.session_state.comments = []

    st.title("YouTube Komentar Manager 🎥")
    
    # Langkah 1: Pilih Channel
    st.header("1. Pilih Channel Aktif")
    user, channels = get_youtube_channels()
    if not channels:
        st.error("Tidak ada channel ditemukan.")
        st.stop()

    channel_titles = [f"{c.title} ({c.subscribers} subs)" for c in channels]
    selected_title = st.selectbox("Pilih salah satu channel:", channel_titles)

    selected_channel = channels[channel_titles.index(selected_title)]
    if st.button("Aktifkan Channel Ini"):
        activate_channel(user, selected_channel.channel_id)
        st.session_state.chosen_channel = selected_channel
        st.success(f"Channel '{selected_channel.title}' berhasil diaktifkan!")

    # Langkah 2: Masukkan link video
    st.header("2. Masukkan Link Video YouTube")
    video_link = st.text_input("Tempelkan link video YouTube kamu di sini:")
    if st.button("Ambil Komentar Mencurigakan"):
        video_id = extract_video_id(video_link)
        if not video_id:
            st.error("Link video tidak valid.")
        else:
            comments, youtube, is_owner = get_suspicious_comments(video_id)
            if not comments:
                st.info("Tidak ada komentar mencurigakan ditemukan.")
            else:
                st.session_state.youtube = youtube
                st.session_state.comments = comments
                st.session_state.is_owner = is_owner
                st.success(f"Ditemukan {len(comments)} komentar mencurigakan.")
                if not st.session_state.is_owner:
                    st.warning("WARNING! Kamu BUKAN pemilik video ini, jadi hanya bisa mereport komen sebagai spam.")

    # Langkah 3: Tampilkan komentar dan beri opsi centang
    if st.session_state.comments:
        st.header("3. Komentar Mencurigakan")
        selected_comments = []
        for comment in st.session_state.comments:
            checked = st.checkbox(f"[{comment['unique_code']}] {comment['author']}: {comment['text']}", key=comment['unique_code'], value=True)
            if checked:
                selected_comments.append(comment)
        if st.session_state.is_owner:
            button_text = "Hapus dan Report Komentar"
        else:
            button_text = "Report Komentar sebagai Spam"
        if st.button(button_text):
            handle_selected_comments(st.session_state.youtube, selected_comments, st.session_state.is_owner)
            st.success("Komentar yang dipilih sudah diproses.")

def login():
    if not login_session_is_valid():
        st.title("Login Page!")
        
        login_clicked = st.button("🔒 Login with Google", key="google_login_button")
        if login_clicked:
            login_user()
            st.success("Login berhasil!")
            st.markdown(refresh, unsafe_allow_html=True)
            main()
    # State untuk menyimpan channel yang dipilih
    else:
          main()


if __name__ == "__main__":
    login()