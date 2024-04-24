Phát hiện Phishing URL
Hiện nay các cuộc tấn công mạng nhắm vào người dùng xảy ra ngày càng nhiều và trầm trọng. Nếu quay về chục năm trước, khi internet chưa được phổ biến như bây giờ, chỉ có những người thật sự giỏi và am hiểu mới có thể sử dụng các kỹ thuật để tấn công nhằm đánh cắp 1 thông tin nào đó thông qua internet. Nhưng đến thời điểm hiện tại, internet được phổ biến khắp nơi dẫn đến việc người dùng có thể bị đánh cắp thông tin bất cứ lúc nào. Có một cách đơn giản và không cần được đào tạo bài bản cũng có thể dùng để lừa đảo, tấn công đánh cắp thông tin cá nhân. Đó chính là URL Phising, hay hiểu đơn giản là lừa người dùng bấm vào đường dẫn (URL), điền thông tin các nhân vào phần đăng nhập,... khi đó kẻ tấn công sẽ có tất cả thông tin người dùng nhập vào mà không tốn tí sức lực nào! Để ngăn chặn điều đó, mô hình học máy dưới đây sẽ được huấn luyện để giúp chúng ta phân biệt và chọn lọc ra các đường dẫn (URL) an toàn.

Các bước thực hiện:

Đọc dữ liệu từ file csv
Trực quan hóa dữ liệu
Tách dữ liệu - chọn lọc các đặc trưng cần thiết
Đào tạo dữ liệu
So sánh mô hình
Kết luận

Cài đặt
1. Sử dụng python bản 3.7
2. pip install -r requirements.txt
3. python app.py
4. Chương trình sẽ được chạy và có đường dẫn: 127.0.0.1:5000
5. Người dùng nhập đường dẫn vào ô input
6.
