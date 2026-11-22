import re
R = {
 'maxillofacial': ('She is a maxillofacial surgeon.', 'A maxillofacial problem affects the jaw and face.', 'Một vấn đề hàm mặt ảnh hưởng đến hàm và khuôn mặt.'),
 'waiting room': ('Please sit in the waiting room.', 'The waiting room is quiet today.', 'Hôm nay phòng chờ yên tĩnh.'),
 'lab': ('The crown is made in the lab.', 'We sent your mold to the lab.', 'Chúng tôi đã gửi mẫu hàm của bạn đến phòng lab.'),
 'staff': ('Our staff is very friendly.', 'All staff wear name badges.', 'Tất cả nhân viên đều đeo bảng tên.'),
 'dental hygienist': ('The dental hygienist cleaned my teeth.', 'The dental hygienist checks your gums first.', 'Chuyên viên vệ sinh răng kiểm tra nướu của bạn trước.'),
 'dental therapist': ('A dental therapist can fill small cavities.', 'Our dental therapist visits schools.', 'Chuyên viên trị liệu nha của chúng tôi đến thăm các trường học.'),
 'burnisher': ('Use the burnisher to smooth the filling.', 'The burnisher has a smooth, round end.', 'Cây miết bóng có đầu tròn và nhẵn.'),
 'mouth': ('Open your mouth, please.', 'Close your mouth slowly.', 'Hãy ngậm miệng lại từ từ.'),
 'gums': ('My gums bleed when I brush.', 'The dentist checked my gums.', 'Nha sĩ đã kiểm tra nướu của tôi.'),
 'hard palate': ('Touch the hard palate with your tongue.', 'The hard palate is made of bone.', 'Khẩu cái cứng được tạo bởi xương.'),
 'soft palate': ('The soft palate moves when you swallow.', 'The soft palate has no bone.', 'Khẩu cái mềm không có xương.'),
 'uvula': ('Say "ah" so I can see your uvula.', 'The uvula is small and soft.', 'Lưỡi gà nhỏ và mềm.'),
 'cementum': ('Cementum covers the root.', 'Cementum is yellow and thin.', 'Xê măng có màu vàng và mỏng.'),
 'periodontal ligament': ('The periodontal ligament holds the tooth in place.', 'Gum disease can damage the periodontal ligament.', 'Bệnh nướu có thể làm hỏng dây chằng nha chu.'),
 'root canal': ('I need a root canal on this tooth.', 'A root canal can save your tooth.', 'Điều trị tủy có thể giữ lại chiếc răng của bạn.'),
 'cut': ('Incisors cut food.', 'The dentist will cut the thread.', 'Nha sĩ sẽ cắt sợi chỉ.'),
 'tear': ('Canines tear meat.', 'Dogs tear meat with their teeth.', 'Chó xé thịt bằng răng.'),
 'crush': ('Premolars crush food.', 'Do not crush the tablet.', 'Đừng nghiền nát viên thuốc.'),
 'chew': ('Chew your food slowly.', 'Chew on the other side today.', 'Hôm nay hãy nhai bên kia.'),
 'face shield': ('A face shield covers your whole face.', 'Clean the face shield after each patient.', 'Lau sạch tấm chắn mặt sau mỗi bệnh nhân.'),
 'reusable': ('Metal tools are reusable after sterilization.', 'This bag is reusable.', 'Cái túi này dùng lại được.'),
 'laser': ('The dentist used a laser on my gums.', 'The laser does not hurt.', 'Tia laser không gây đau.'),
 'business hours': ('Our business hours are 8 a.m. to 5 p.m.', 'The clinic is closed outside business hours.', 'Phòng khám đóng cửa ngoài giờ làm việc.'),
 'payment': ('We accept payment by card.', 'Thank you for your payment.', 'Cảm ơn bạn đã thanh toán.'),
 'authorization': ('We need authorization from your insurance.', 'We are waiting for authorization.', 'Chúng tôi đang chờ giấy chấp thuận.'),
 'eye contact': ('Make eye contact when you talk.', 'Some patients avoid eye contact.', 'Một số bệnh nhân tránh nhìn vào mắt.'),
 'listen': ('Please listen to the patient.', 'Listen to your body when it hurts.', 'Hãy lắng nghe cơ thể khi bị đau.'),
 'daily': ('Floss daily.', 'Daily brushing keeps decay away.', 'Đánh răng hằng ngày giúp tránh sâu răng.'),
 'toothbrush': ('Change your toothbrush every three months.', 'Do not share your toothbrush.', 'Đừng dùng chung bàn chải đánh răng.'),
 'mouthwash': ('Rinse with mouthwash after brushing.', 'This mouthwash has no alcohol.', 'Nước súc miệng này không có cồn.'),
 'plaque': ('Brushing removes plaque.', 'Plaque turns into tartar.', 'Mảng bám biến thành cao răng.'),
 'scrape': ('The hygienist will scrape the tartar off.', 'This tool can scrape the root clean.', 'Dụng cụ này có thể cạo sạch chân răng.'),
 'spit': ('Please spit into the sink.', 'Do not spit on the floor.', 'Đừng nhổ ra sàn.'),
}
for f in ('ex1.txt', 'ex2.txt', 'ex3.txt'):
    lines = open(f, encoding='utf8').read().split('\n'); cur = None
    for i, ln in enumerate(lines):
        if ln.startswith('@'): cur = ln[1:].strip(); continue
        if R.get(cur) and ln.startswith('= '):
            en = ln[2:].split(' => ')[0].strip()
            if en == R[cur][0]: lines[i] = f'= {R[cur][1]} => {R[cur][2]}'; R[cur] = None
    open(f, 'w', encoding='utf8').write('\n'.join(lines))
left = [k for k, v in R.items() if v]
print('chưa thay:', left)
