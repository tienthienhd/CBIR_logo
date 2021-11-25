# [CBIR] Dự án so sánh logo, phát hiện logo

## Tài liệu hướng dẫn:

**Mục đích chính của dự án:**

- So sánh xem 2 ảnh đầu vào có phải cùng một logo hay không, nếu có sẽ in ra logo cần tìm
- Kiểm tra trong bức ảnh có phát hiện logo được yêu cầu

**Các chức năng phụ:**

- Thêm hình ảnh logo vào file dữ liệu
- Xóa toàn bộ ảnh của logo được chỉ định trong file dữ liệu

## 1. Cách cài đặt tại local:
### 1.1. Cài đặt python3, pip:
**python**:
- Đối với hệ điều hành window, xem hướng dẫn chi tiết tại: https://phoenixnap.com/kb/how-to-install-python-3-windows
- Đối với hệ điều hành ubuntu, xem hướng dẫn chi tiết tại: https://phoenixnap.com/kb/how-to-install-python-3-ubuntu <br>

**pip**:
- Đối với hệ điều hành window, xem hướng dẫn chi tiết tại: https://phoenixnap.com/kb/install-pip-windows
- Đối với hệ điều hành ubuntu, xem hướng dẫn chi tiết tại: https://linuxize.com/post/how-to-install-pip-on-ubuntu-20.04/

### 1.2. Cài đặt môi trường:
Tại thư mục CBIR_logo, thực hiện lệnh trên command line để cài đặt toàn bộ thư viện sử dụng và các gói liên quan, cụ thể như sau:
```bash
pip install -r requirement.txt
```
Tại file **main.py**, địa chỉ IP mặc định là **host**: [ 0.0.0.0](localhost), cổng **port**: [5000](), để thay đổi thì sửa lại **host** và **port** tương ứng, tại dòng 250 của file.<br>
Cuối cùng, tại command line, thực hiện chạy lệnh sau để chạy chương trình:
```bash
python main.py
```
Thực hiện test API, được mô tả chi tiết ở file **README.md** (file cùng thư mục với file **main.py**):
- Check có logo trong ảnh
- Check 2 ảnh có cùng logo 
- Thêm ảnh vào file dữ liệu logo đối sánh (**Yêu cầu**: cắt ảnh chỉ chứa logo cần check, không chứa các background không cần thiết, các yêu cầu liên quan đã nêu ở mục _2.1.1_)
- Xóa toàn bộ logo cần đối sánh

## 2. Hướng dẫn cách sử dụng test trên swagger:

### 2.1. Thêm hình ảnh logo vào file dữ liệu:
**_Truy cập vào trang [http://46.137.245.145:5000](http://46.137.245.145:5000/api/docs/) để bắt đầu test_**
#### 2.1.1. Mô tả:

Đầu vào gồm tập hợp các ảnh chỉ chứa vùng logo, **YÊU CẦU**:

- **Số lượng ảnh tối thiểu** mỗi loại logo: 20 ảnh / loại logo
    - Ví dụ: Đối với logo của pepsi có nhiều loại, ví dụ 3 loại là logo trên nền đen, logo trên nền trắng, logo trên nền
      xanh. Đối với mỗi loại cần tối thiểu 20 ảnh thêm vào file dữ liệu, vậy tổng số lượng ảnh thêm vào của logo pepsi
      là 60 ảnh.
      **Chú ý:** Số lượng ảnh càng nhiều dẫn đến quá trình đọc càng chậm, do đó **số lượng thêm tối đa** của mỗi loại là
      100 ảnh
    - Do sự đa dạng của mỗi logo khác nhau nên cần linh động về số lượng ảnh mỗi loại của logo
- Đối với mỗi bức ảnh, ảnh cắt chỉ nên chứa vùng **logo cần nhận diện** và thương hiệu đi kèm (nếu có)
- Ảnh thêm vào nên cắt ảnh có chất lượng không quá kém, kích thước không quá bé không quá lớn:
    - Dung lượng lý tưởng: 20KB - 200KB
    - Kích thước lý tưởng: 100px - 300px (tùy theo chiều ngang và chiều dọc của vùng chứa logo)
    - Ví dụ: Hình ảnh pepsi có dung lượng 22.4KB, kích thước chiều cao x chiều rộng tương ứng là: (113px, 90px)

      ![](./pepsilogo.jpg)
- Hình ảnh logo nên đa dạng góc quay, kích thước.

#### 2.1.2. Các bước thêm logo:
- Bước 1: Truy cập vào trang web đã được nêu ở trên
- Bước 2: Chọn mục add-logo
- Bước 3: Ấn vào button **_Try it out_** để thực hiện, gồm 2 bước:
  - **_Choose File_** để chọn file ảnh cần thêm
  - Điền vào **_tên logo_** cần thêm
- **Chú ý**: Hai thông tin này đều bắt buộc phải có

### 2.2. Xóa toàn bộ ảnh của logo được chỉ định trong file dữ liệu:

Đầu vào là tên của **logo cần xóa**. Sau khi gửi yêu cầu, toàn bộ thông tin (ảnh, thông tin nhận dạng) của logo yêu cầu
đều bị xóa. Khi thực hiện xong thì không thể khôi phục lại thông tin bị xóa. Tuy nhiên, vẫn có thể thêm lại thông tin
như mô tả ở mục trên, tiến hành thực hiện các bước thêm ảnh như trên.



