# bot_follow_and_post_twitter-server-interface

Cách sử dụng bot tự động đăng bài lên twitter

1. mở file input.xlsx.

![1705551475652](image/README/1705551475652.png)

![1705551571523](image/README/1705551571523.png)

Ở sheet 500+ connection

A. CEO's Twitter: hãy để đường dẫn URL tới profile accounts follow

B. Tweet at CEO: điền tên của bài tweet lấy từ sheet "tweet"

C. TAG: Tag người khác vào bài tweet, hãy điền vào userId, ví dụ: HaoNam19307, JamesPGorman1

D. HashTAG:  ví dụ: heath, donation
	Số lượng tag và hashtag xuất hiện tùy vào số lượng ký tự "&" và "#" tương tự trong Tweet ở sheet "tweet"

E. Personal Tweet: điền tên của bài tweet lấy từ sheet "tweet"

F, G. Tương tự C,D

Ở sheet tweet

A. đặt tên cho bài tweet (không để trùng tên)

B. Nội dung bài tweet.

	dấu & sẽ được chương trình thay thế lần lượt cho các TAG ở sheet 500+ connection
	dấu # sẽ được chương trình thay thế lần lượt cho các HASHTAG
	số lượng dấu & và # có thể them theo ý muốn và vị trí bất kỳ.
 
C. thêm hình ảnh cho bài tweet.

	Để lấy đúng đường dẫn hình ảnh hãy: chuột phải hình ảnh -> chọn properties -> chọn Security
	hoặc lấy đường dẫn theo cách nào khác bạn biết
	chỉ thêm được 1 hình ảnh cho 1 bài viết

2. Chạy file twitter.exe nằm ở cùng folder.
   Một trình duyệt sẽ xuất hiện, hãy đăng nhập vào twitter.
   Sau khi đăng nhập thành công sẽ xuất hiện cửa sổ dưới

![1705552006146](image/README/1705552006146.png)

    * Starting Row và Ending Row: Nhập vào số dòng User muốn bắt đầu và kết thúc ở sheet 500+ connection
	ví dụ: nếu nhập 1 và 3 thì chương trình sẽ chọn 3 dòng dữ liệu đầu tiên ở sheet 500+ connection
    * Follow the Twitter user only: Chỉ follow các Profile bạn đã chọn.
    * Follow and Tweet at the Twitter user: Follow và đăng bài viết các dòng đã chọn
    * Personal Tweets: Đăng bài viết cá nhân theo các dòng đã chọn
    * Ô message: Các bài viết quá dài sẽ không đăng được và note lại ở đây. Hãy theo dõi để sửa.

*Kết quả của một bài viết đúng.

![1705553150699](image/README/1705553150699.png)
