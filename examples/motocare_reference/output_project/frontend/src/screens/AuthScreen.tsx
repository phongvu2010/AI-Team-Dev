import React, { useState } from 'react';
import { View, Text, TextInput, TouchableOpacity, StyleSheet, Alert } from 'react-native';

interface AuthScreenProps {
  onLoginSuccess: (token: string) => void;
}

export const AuthScreen: React.FC<AuthScreenProps> = ({ onLoginSuccess }) => {
  const [phone, setPhone] = useState('0912345678');
  const [password, setPassword] = useState('SecurePass123!');
  const [isRegister, setIsRegister] = useState(false);

  const handleSubmit = () => {
    if (!phone || !password) {
      Alert.alert('Lỗi', 'Vui lòng điền đủ thông tin');
      return;
    }
    const token = `jwt_mock_${phone}`;
    onLoginSuccess(token);
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>{isRegister ? 'Đăng Ký Tài Khoản' : 'Đăng Nhập Khách Hàng'}</Text>
      <TextInput style={styles.input} placeholder="Số điện thoại (09...)" value={phone} onChangeText={setPhone} keyboardType="phone-pad" />
      <TextInput style={styles.input} placeholder="Mật khẩu" value={password} onChangeText={setPassword} secureTextEntry />
      <TouchableOpacity style={styles.btn} onPress={handleSubmit}>
        <Text style={styles.btnText}>{isRegister ? 'Tạo Tài Khoản' : 'Đăng Nhập'}</Text>
      </TouchableOpacity>
      <TouchableOpacity style={styles.toggleBtn} onPress={() => setIsRegister(!isRegister)}>
        <Text style={styles.toggleText}>{isRegister ? 'Đã có tài khoản? Đăng nhập' : 'Chưa có tài khoản? Đăng ký'}</Text>
      </TouchableOpacity>
    </View>
  );
};

const styles = StyleSheet.create({
  container: { flex: 1, padding: 24, justifyContent: 'center', backgroundColor: '#FFFFFF' },
  title: { fontSize: 22, fontWeight: 'bold', marginBottom: 20, textAlign: 'center', color: '#0F172A' },
  input: { borderWidth: 1, borderColor: '#CBD5E1', borderRadius: 8, padding: 12, marginBottom: 14, fontSize: 16 },
  btn: { backgroundColor: '#0284C7', padding: 14, borderRadius: 8, alignItems: 'center' },
  btnText: { color: '#FFFFFF', fontWeight: 'bold', fontSize: 16 },
  toggleBtn: { marginTop: 16, alignItems: 'center' },
  toggleText: { color: '#0284C7', fontSize: 14 },
});
