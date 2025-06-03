# Do_an_AI_ca_nhan_cuoi_ki

ĐỒ ÁN CÁ NHÂN MÔN TRÍ TUỆ NHÂN TẠO
Giảng viên hướng dẫn: TS.Phan Thị Huyền Trang
Sinh viên thực hiện: Phan Đình Sáng
Mã số sinh viên: 23110303
Mã lớp học: ARIN330585_04
Học kỳ II năm học 2024-2025

MỤC LỤC
NỘI DUNG CHÍNH	2
1. Giới thiệu bài toán	2
2. Mục tiêu	2
3. Một số thuật toán sử dụng	2
    3.1. Tìm kiếm không có thông tin	2
    3.2. Tìm kiếm có thông tin	4
    3.3. Thuật toán tìm kiếm cục bộ	6
    3.4. Thuật toán tìm kiếm trong môi trường phức tạp	8
    3.5. Thuật toán tìm kiếm có ràng buộc	11
    3.6. Thuật toán tìm kiếm học tăng cường	13
4. Kết luận	14
5. Tài liệu tham khảo	14




NỘI DUNG CHÍNH

1. Giới thiệu bài toán

"Bài toán 8-puzzle là một dạng phổ biến của bài toán xếp gạch trượt (sliding tile puzzle), thường được sử dụng như một môi trường thử nghiệm cho các thuật toán tìm kiếm. Bài toán bao gồm một ma trận 3x3 chứa chín vị trí, trong đó tám vị trí được lấp đầy bởi các chữ số duy nhất từ 1 đến 8, và một vị trí là ô trống (đại diện bằng số 0). Mỗi cấu hình của ma trận này được gọi là một 'trạng thái'.
Mục tiêu của bài toán là biến đổi một trạng thái ban đầu cho trước thành một trạng thái mục tiêu mong muốn thông qua một chuỗi các 'hành động'. Hành động duy nhất được phép là di chuyển ô trống. Ô trống có thể được hoán đổi vị trí với ô vuông liền kề (theo chiều ngang hoặc dọc), miễn là ô liền kề đó nằm trong phạm vi lưới. Các hướng di chuyển khả thi bao gồm lên, xuống, trái và phải.
Thách thức nằm ở việc tìm ra một đường đi (một chuỗi các hành động) từ trạng thái ban đầu đến trạng thái mục tiêu. Các thuật toán tìm kiếm khác nhau (như BFS, DFS, A*, v.v.) có thể được áp dụng để giải bài toán này, mỗi thuật toán sẽ dẫn đến hiệu quả khác nhau về số lượng bước cần thiết để đạt được mục tiêu, thời gian tính toán, lượng bộ nhớ sử dụng, và thậm chí là khả năng tìm thấy lời giải trong những trường hợp phức tạp."
2. Mục tiêu

Mục tiêu của nghiên cứu/dự án này là áp dụng các thuật toán tìm kiếm trí tuệ nhân tạo đã được học để giải quyết một bài toán cụ thể. Từ đó, tiến hành đánh giá chi tiết hiệu suất và hiệu quả của từng thuật toán về mặt thời gian thực thi và không gian bộ nhớ sử dụng trong các trường hợp khác nhau, làm cơ sở cho việc phân tích và so sánh ưu nhược điểm của chúng. 
Từ đây, hoàn toàn có thể áp dụng các thuật toán này vào các bài toán thực tiễn như tìm đường đi giữa các thành phố, tìm kiếm thông tin nhanh chóng hơn trong kho dữ liệu lớn, lập lịch, học máy…(1)
3. Một số thuật toán sử dụng

3.1. Tìm kiếm không có thông tin

Các thành phần chính của bài toán tìm kiếm

Bài toán 8-puzzle nhận đầu vào là trạng thái ban đầu, được định nghĩa bởi một ma trận 3x3 chứa các số từ 0 đến 8 không trùng lặp (với 0 là ô trống).
Mục tiêu của bài toán là chuyển đổi trạng thái ban đầu này thành trạng thái mục tiêu mong muốn (cũng là một ma trận 3x3 tương tự) bằng cách di chuyển ô trống.
Hành động: Các hành động có thể thực hiện từ một trạng thái, bao gồm di chuyển ô trống theo bốn hướng: 'Up', 'Down', 'Left', 'Right'.
Tổng chi phí của đường đi từ trạng thái ban đầu đến trạng thái đang xét, thường ký hiệu là g(state)(2).
Giải pháp là một đường đi chứa các trạng thái với trạng thái đầu tiên là trạng thái ban đầu, các trạng thái biến đổi sau khi thực hiện hành động lên trạng thái ban đầu và trạng thái cuối cùng là trạng thái mục tiêu (trạng thái cần tìm).
* Thuật toán BFS

BFS - Breadth-First Search (Tìm kiếm theo chiều rộng): Khám phá các trạng thái theo mức độ, có thể được dùng khi các hành động có cùng chi phí, đảm bảo tìm được giải pháp ngắn nhất nếu tồn tại giải pháp. Thuật toán này dùng hàng đợi để lưu trữ các trạng thái đang được xét theo nguyên tắc FIFO (vào trước ra trước). Thuật toán kết thúc khi tìm ra lời giải hoặc khi hàng đợi rỗng.(2)

* Thuật toán DFS
DFS - Depth-First Search (Tìm kiếm theo chiều sâu): Khi các hành động có cùng chi phí có thể áp dụng thuật toán này để Khám phá sâu vào các nhánh trước khi quay lại xét nhánh kế tiếp. Thuật toán có thể tìm ra được lời giải nhưng không đảm bảo tìm được giải pháp tối ưu do có thể phải xét hết tất cả các trạng thái trên nhánh không có lời giải, sau đó mới chuyển sang các nhánh khác.

* Thuật toán UCS - Uniform Cost Search

UCS - Uniform Cost Search (Tìm kiếm theo chi phí đồng nhất): Mở rộng từ một trạng thái tới trạng thái có chi phí tốt nhất từ trạng thái gốc đến trạng thái đó, đảm bảo tìm được giải pháp tối ưu với chi phí hành trình tìm kiếm là thấp nhất do tính chi phí các nút lân cận và sau đó mới di chuyển đến nút có chi phí tốt nhất.

* Thuật toán IDS

IDS - Iterative Deepening Search (Tìm kiếm sâu dần): Thuật toán này ‘kết hợp ưu điểm của tìm kiếm theo chiều rộng và chiều sâu, thuật toán tìm kiếm theo chiều sâu từ mức thấp đến mức cao hơn, đến khi tìm ra giải pháp’. Đây là lựa chọn tối ưu với “các bài toán tìm kiếm khi không biết trước độ sâu của lời giải”(3).

Hình ảnh so sánh hiệu suất của các thuật toán




Nhận xét về hiệu suất của các thuật toán trong nhóm

Các thuật toán tìm kiếm không thông tin, chẳng hạn như Tìm kiếm theo chiều rộng (BFS), Tìm kiếm theo chiều sâu (DFS), Tìm kiếm theo chiều sâu lặp (IDS), và Tìm kiếm chi phí đồng nhất (UCS), cho thấy hiệu năng khác nhau khi giải quyết bài toán như 8-puzzle. Nhìn chung, do thiếu thông tin hướng dẫn, chúng có xu hướng khám phá một phần lớn không gian trạng thái.
Về thời gian thực thi, UCS thường là thuật toán chậm nhất trong nhóm trong trường hợp tổng quát do cần mở rộng các nút theo thứ tự chi phí. DFS có thể rất không hiệu quả về thời gian nếu lời giải nằm sâu trong một nhánh ít được ưu tiên thăm trước, hoặc nếu không gian trạng thái rất sâu. BFS và IDS có thời gian phụ thuộc vào cấu trúc bài toán và độ sâu lời giải, với IDS thường thể hiện sự cân bằng tốt giữa thời gian và không gian.
Liên quan đến chất lượng lời giải (thường đo bằng số bước di chuyển hoặc tổng chi phí), cả BFS và IDS đều đảm bảo tìm được lời giải có độ dài đường đi tối ưu (số bước ít nhất) đối với bài toán 8-puzzle (nơi mỗi bước có chi phí bằng 1). UCS đảm bảo tìm được lời giải có tổng chi phí tối ưu. Ngược lại, DFS không đảm bảo tính tối ưu về độ dài hay chi phí đường đi; nó có thể tìm thấy một lời giải rất dài.
3.2. Tìm kiếm có thông tin

Các thành phần chính của bài toán tìm kiếm

Bài toán 8 puzzle có trạng thái ban đầu là ma trận 3×3 chứa 9 chữ số từ 0 đến 8 không trùng lặp (với số 0 đại diện cho ô trống) là đầu vào bài toán cần giải quyết.
Bài toán 8 puzzle có trạng thái mục tiêu cũng là ma trận 3×3 chứa 9 chữ số từ 0 đến 8 không trùng lặp (với số 0 đại diện cho ô trống) là đầu ra của bài toán (là trạng thái muốn có sao khi thực hiện các hành động từ trạng ban đầu).
Hành động: Các hành động có thể thực hiện từ một trạng thái, bao gồm di chuyển ô trống theo bốn hướng: 'Up', 'Down', 'Left', 'Right'
Giải pháp là một đường đi chứa các trạng thái với trạng thái đầu tiên là trạng thái ban đầu, các trạng thái biến đổi sau khi thực hiện hành động lên trạng thái ban đầu và trạng thái cuối cùng là trạng thái mục tiêu (trạng thái cần tìm).
Thuật toán Greedy

Greedy Search (Tìm kiếm tham lam - tìm kiếm Greedy): Mở rộng trạng thái tới trạng thái có giá trị hàm heuristic tốt nhất (trong đó, hàm heuristic là hàm đánh giá chi phí từ trạng thái đang xét đến trạng đích).

*Thuật toán A*

A-Star Search (Tìm kiếm A*): Tìm kiếm bằng cách tính chi phí từ trạng thái ban đầu đến trạng thái hiện tại và ước lượng chi phí từ trạng thái hiện tại đến trạng thái mục tiêu để tìm ra trạng thái tiếp theo có chi phí tốt nhất để di chuyển đến.

* Thuật toán Iterative Deepening A* (IDA*)


Hình ảnh so sánh hiệu suất của các thuật toán




Nhận xét về hiệu suất của các thuật toán trong nhóm

Sự vượt trội về tốc độ của nhóm thuật toán tìm kiếm có thông tin so với nhóm không thông tin đến từ việc sử dụng hàm heuristic làm kim chỉ nam. Heuristic giúp định hướng quá trình tìm kiếm, tập trung vào các khu vực có khả năng chứa lời giải cao. Tuy nhiên, ngay trong nhóm này cũng tồn tại những sự đánh đổi về hiệu quả:
Greedy ưu tiên tốc độ: Nó chỉ dựa vào hàm heuristic để chọn nút mở rộng tiếp theo. Điều này giúp nó thường tìm thấy một lời giải rất nhanh (ít thời gian thực thi và ít trạng thái thăm được), nhưng không đảm bảo lời giải đó là tối ưu (số bước có thể rất lớn). Greedy dễ bị mắc kẹt ở các 'cực trị cục bộ'.
A Search* ưu tiên tính tối ưu: Bằng cách kết hợp cả chi phí đã di chuyển (g(n)) và ước lượng chi phí còn lại (h(n)) thông qua hàm đánh giá f(n), A* đảm bảo tìm được lời giải tối ưu (đường đi ngắn nhất/chi phí thấp nhất) với điều kiện heuristic phù hợp. Tuy nhiên, việc này đòi hỏi phải xem xét nhiều trạng thái hơn, dẫn đến thời gian thực thi và bộ nhớ sử dụng thường cao hơn Greedy.
IDA Search* là giải pháp cân bằng: IDA* kết hợp ưu điểm tối ưu của A* và hiệu quả không gian của DFS. Nó tìm được lời giải tối ưu như A*, nhưng tiêu thụ ít bộ nhớ hơn đáng kể. Mặc dù có thể mở rộng lại một số nút qua các lần lặp, IDA* thường thể hiện hiệu quả tốt về thời gian trong thực tế, đặc biệt trong các bài toán có bộ nhớ hạn chế.
Như vậy, trong khi Greedy phù hợp khi tốc độ là ưu tiên hàng đầu và chấp nhận lời giải không tối ưu, A* và IDA* được sử dụng khi cần tìm lời giải tối ưu, với IDA* là lựa chọn tốt khi bộ nhớ là yếu tố hạn chế.
3.3. Thuật toán tìm kiếm cục bộ

Các thành phần chính của bài toán tìm kiếm

Bài toán 8 puzzle có trạng thái ban đầu là ma trận 3×3 chứa 9 chữ số từ 0 đến 8 không trùng lặp (với số 0 đại diện cho ô trống) là đầu vào bài toán cần giải quyết.
Bài toán 8 puzzle có trạng thái mục tiêu cũng là ma trận 3×3 chứa 9 chữ số từ 0 đến 8 không trùng lặp (với số 0 đại diện cho ô trống) là đầu ra của bài toán (là trạng thái muốn có sao khi thực hiện các hành động từ trạng ban đầu).
Hành động: Các hành động có thể thực hiện từ một trạng thái, bao gồm di chuyển ô trống theo bốn hướng: 'Up', 'Down', 'Left', 'Right'
Giải pháp là một đường đi chứa các trạng thái với trạng thái đầu tiên là trạng thái ban đầu, các trạng thái biến đổi sau khi thực hiện hành động lên trạng thái ban đầu và trạng thái cuối cùng là trạng thái mục tiêu (trạng thái cần tìm).
Thuật toán Simple hill climbing

Thuật toán leo đồi đơn giản đánh giá từng trạng thái lân cận một cách tuần tự và chọn trạng thái đầu tiên tối ưu hơn so với trạng thái hiện tại.

*Thuật toán Steppest ascent hill climbing

Thuật toán leo đồi dốc nhất đánh giá tất cả các trạng thái lân cận và chọn trạng thái mang lại cải thiện lớn nhất so với trạng thái hiện tại.

*Thuật toán Stochastic hill climbing

Thuật toán leo đồi ngẫu nhiên chọn ngẫu nhiên một trạng thái lân cận và quyết định chuyển sang trạng thái đó nếu nó tốt hơn trạng thái hiện tại.

*Thuật toán Beam Search

Thuật toán Genetic Algorithm
So sánh thời gian thực thi của các thuật toán

Nhận xét về hiệu suất của các thuật toán trong nhóm

Nhóm thuật toán tìm kiếm cục bộ hoạt động bằng cách thăm dò không gian lân cận của trạng thái hiện tại để tìm kiếm sự cải thiện, khác với việc duyệt toàn bộ cây tìm kiếm trạng thái. Nhược điểm chính của chúng là dễ mắc kẹt tại các cực trị địa phương, không tìm được lời giải tối ưu toàn cục. So sánh cụ thể:
Hill Climbing (Simple, Steepest, Stochastic): Nhanh nhất về thời gian thực thi và tiết kiệm bộ nhớ nhất, nhưng hầu như không tìm được lời giải tối ưu do rất dễ bị kẹt tại cực trị địa phương.
Simulated Annealing: Có khả năng thoát khỏi cực trị địa phương và tìm được lời giải tối ưu toàn cục, nhưng chậm hơn Hill Climbing do cơ chế thăm dò ngẫu nhiên. Tiêu thụ ít bộ nhớ.
Beam Search: Cân bằng giữa Hill Climbing và các phương pháp phức tạp hơn. Khám phá không gian rộng hơn Hill Climbing (nhờ beam width k), giúp tăng khả năng tìm được lời giải tốt và tránh bị kẹt như Hill Climbing đơn giản. Tuy nhiên, nó tốn thời gian và bộ nhớ hơn Hill Climbing do phải quản lý và lọc k trạng thái tốt nhất.
3.4. Thuật toán tìm kiếm trong môi trường phức tạp

Các thành phần chính của bài toán tìm kiếm

Trạng thái ban đầu là một tập các ma trận 3×3 chứa 9 chữ số từ 0 đến 8 không trùng lặp (với số 0 đại diện cho ô trống) là đầu vào bài toán cần giải quyết.
Trạng thái mục tiêu cũng là một tập ma trận 3×3 chứa 9 chữ số từ 0 đến 8 không trùng lặp (với số 0 đại diện cho ô trống) là đầu ra của bài toán (là trạng thái muốn có sao khi thực hiện các hành động từ trạng ban đầu).
Hành động: Các hành động có thể thực hiện từ một trạng thái, bao gồm di chuyển ô trống theo bốn hướng: 'Up', 'Down', 'Left', 'Right'
Giải pháp phép biến đổi tập trạng thái ban đầu thành thành tập trạng thái mục tiêu bằng việc sử dụng một trong các thuật toán của các nhóm phần trên.
Thuật toán tìm kiếm AND - OR search


Thuật toán tìm kiếm không có sự quan sát (search with no observation)


Thuật toán tìm kiếm có sự quan sát một phần (search with partial observation)


Hình ảnh so sánh hiệu suất của các thuật toán




Nhận xét về hiệu suất của các thuật toán trong nhóm

So với thuật toán tìm kiếm mù (không có quan sát), thuật toán tìm kiếm có quan sát một phần thể hiện những ưu điểm rõ rệt về hiệu quả thực thi. Về thời gian xử lý, việc sử dụng thông tin quan sát được (dù chỉ là một phần) giúp thuật toán định hướng và thu hẹp không gian tìm kiếm khả thi một cách hiệu quả, từ đó tăng tốc độ tính toán và giảm đáng kể thời gian cần thiết để tìm ra lời giải.
Về chất lượng lời giải, cả hai phương pháp đều có khả năng tìm được lời giải tối ưu như nhau xét về kết quả cuối cùng. Tuy nhiên, khi đối mặt với các bài toán có độ phức tạp cao hơn (thể hiện qua trạng thái bắt đầu và đích khó khăn), thuật toán tìm kiếm mù thường gặp thách thức lớn hơn và có tỷ lệ không tìm thấy lời giải cao hơn đáng kể. Điều này là do thuật toán tìm kiếm có quan sát một phần có thể sử dụng thông tin đích đã biết để loại bỏ sớm các nhánh trạng thái không khả thi, giúp quá trình tìm kiếm tập trung và hiệu quả hơn, qua đó tăng tỷ lệ thành công trong việc giải quyết các bài toán khó.
Cuối cùng, xét về số lượng trạng thái cần duyệt, thuật toán tìm kiếm có quan sát một phần cho thấy sự giảm thiểu đáng kể. Đây là lợi thế cực kỳ quan trọng đối với các bài toán có không gian trạng thái cực lớn, điển hình như bài toán 8-puzzle. Việc tận dụng thông tin quan sát không chỉ làm giảm chi phí tính toán mà còn hướng thuật toán đến các khu vực trong không gian trạng thái có khả năng chứa lời giải cao hơn, tối ưu hóa quá trình tìm kiếm tổng thể.
3.5. Thuật toán tìm kiếm có ràng buộc

Các thành phần chính của bài toán tìm kiếm

Tập các biến: Mỗi ô vuông trong bảng 3x3 được xem là một biến. Gọi các biến lần lượt là X1 đến X9 tương ứng với 9 ô cần điền giá trị (giá trị 0 tượng trưng cho ô trống)
Miền giá trị: Mỗi biến Xi có miền giá trị là một số trong tập {0,1,2,3,4,5,6,7,8}
Ràng buộc:
Tính duy nhất: Mỗi số từ 0 đến 8 chỉ xuất hiện đúng 1 lần trên toàn bộ bảng
Tính hợp lệ: Số cần điền mỗi ô phải nằm trong miền giá trị của ô
Thuật toán kiểm thử


Thuật toán backtracking


Thuật toán AC3
So sánh thời gian thực thi giữa các thuật toán

Nhận xét về hiệu suất của các thuật toán trong nhóm

Trong việc giải các Bài toán Thỏa mãn Ràng buộc (CSP), hiệu suất của các thuật toán như AC3, Backtracking và các phương pháp thử nghiệm đơn giản có sự phân hóa rõ rệt. Về thời gian thực thi, AC3 và Backtracking đều hoạt động rất nhanh chóng, cho thấy khả năng định vị lời giải hiệu quả. Nổi bật nhất là AC3, với thời gian thực thi thường là thấp nhất. Điều này đạt được nhờ cơ chế lọc miền giá trị chủ động: AC3 loại bỏ sớm các giá trị cho biến mà chắc chắn không thể dẫn đến lời giải cuối cùng dựa trên các ràng buộc, giúp giảm đáng kể không gian tìm kiếm ngay từ đầu. Ngược lại, các thuật toán thử nghiệm đơn giản (như gán giá trị ngẫu nhiên rồi kiểm tra) có thời gian thực thi cao hơn đáng kể bởi bản chất là sinh-và-kiểm tra (generate-and-test); chúng thực hiện việc gán giá trị một cách ít có định hướng trước khi kiểm tra xem cấu hình đó có thỏa mãn ràng buộc hay không.
Về số bước thực hiện để tìm ra lời giải, AC3 yêu cầu ít bước nhất do không gian tìm kiếm đã được thu hẹp tối đa nhờ việc lọc miền giá trị. Backtracking có số bước nhiều hơn AC3 nhưng vẫn hiệu quả hơn đáng kể so với phương pháp thử nghiệm đơn giản, nhờ cơ chế quay lui hiệu quả khi gặp trạng thái không khả thi. Phương pháp thử nghiệm đơn giản phải thực hiện số bước cao nhất và lãng phí nhiều công sức vào việc khám phá các trạng thái không thỏa mãn do thiếu định hướng và không học hỏi từ các thất bại trước đó. Tóm lại, sự khác biệt về hiệu suất chủ yếu đến từ khả năng chủ động xử lý và tận dụng ràng buộc để thu hẹp không gian tìm kiếm và tránh các nhánh không xử lý được.

3.6. Thuật toán tìm kiếm học tăng cường

Các thành phần chính của bài toán tìm kiếm

Trạng thái ban đầu là một tập các ma trận 3×3 chứa 9 chữ số từ 0 đến 8 không trùng lặp (với số 0 đại diện cho ô trống) là đầu vào bài toán cần giải quyết.
Trạng thái mục tiêu cũng là một tập ma trận 3×3 chứa 9 chữ số từ 0 đến 8 không trùng lặp (với số 0 đại diện cho ô trống) là đầu ra của bài toán (là trạng thái muốn có sao khi thực hiện các hành động từ trạng ban đầu).
Hành động: Các hành động có thể thực hiện từ một trạng thái, bao gồm di chuyển ô trống theo bốn hướng: 'Up', 'Down', 'Left', 'Right'
Phần thưởng: Giá trị số nhận được sau khi thực hiện một hành động từ một trạng thái.
Bảng Q: Bảng lưu trữ giá trị Q cho mỗi cặp trạng thái - hành động, đại diện cho kỳ vọng phần thưởng khi thực hiện hành động đó từ trạng thái tương ứng.
Tập huấn luyện: Một chuỗi các bước từ trạng thái ban đầu đến khi đạt trạng thái mục tiêu hoặc vượt quá số bước tối đa.
Thuật toán tìm kiếm Q Learning

Nhận xét về hiệu suất của thuật toán

Phần thưởng tăng mạnh trong giai đoạn đầu (khoảng 1000 episode đầu tiên), sau đó duy trì ổn định gần mức tối đa (xấp xỉ 100). Phần thưởng tăng đồng nghĩa với việc tác nhân (agent) dần học được cách giải bài toán.
Tỷ lệ thành công tăng từ dưới 20% lên gần 100% trong khoảng 1000-2000 episode. Điều này cho thấy thuật toán học cách giải đúng puzzle gần như mọi lần sau một số lượng episode huấn luyện nhất định.
Số bước trung bình ban đầu rất cao (trên 17000 bước), sau đó giảm nhanh xuống dưới 1000 bước và dao động quanh mức thấp. Cho thấy tác nhân ban đầu hành động ngẫu nhiên, sau đó dần tối ưu hóa để giải puzzle với ít bước hơn.
4. Kết luận

Đa phần các thuật toán AI đã giải quyết khá tốt bài toán 8-puzzle. Mỗi thuật toán sẽ có ưu, nhược điểm khác nhau về các tiêu chí như thời gian thực thi, số bước lời giải, số trạng thái thăm và hoàn toàn có thể được kết hợp lẫn nhau để tăng hiệu quả giải quyết bài toán.
Thông qua dự án này, ta hoàn toàn có thể áp dụng để giải quyết các thuật toán thực tế khác trong đời sống nhằm cải thiện hiệu quả và chất lượng lời giải.
5. Tài liệu tham khảo

(1). Elastic Platform Team, "Understanding AI search algorithms", elastic,  ngày 21 tháng 3 năm 2024 (truy cập ngày 17 tháng 5 năm 2025)
(2). Stuart Russell and Peter Norvig, "Russell 2020 Artificial intelligence a modern approach"
(3). "Các thuật toán tìm kiếm: chìa khóa mở cửa trí tuệ nhân tạo", KDATA, https://kdata.vn/tin-tuc/cac-thuat-toan-tim-kiem-chia-khoa-mo-cua-tri-tue-nhan-tao, (truy cập ngày 17 tháng 5 năm 2025)
