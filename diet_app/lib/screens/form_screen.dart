import 'package:flutter/material.dart';
import 'result_screen.dart';
import '../services/api_service.dart';

class FormScreen extends StatefulWidget {
  const FormScreen({super.key});

  @override
  State<FormScreen> createState() => _FormScreenState();
}

class _FormScreenState extends State<FormScreen> {
  final _nameController = TextEditingController();
  final _ageController = TextEditingController();
  final _weightController = TextEditingController();
  final _heightController = TextEditingController();
  final _restrictionsController = TextEditingController();

  String _gender = 'Male';
  String _activityLevel = 'Hareketsiz';
  String _goal = 'Kilo ver';
  int _frequency = 3;
  int _experience = 1;
  double _sessionHours = 1.0;
  String _equipment = 'Spor salonu';
  bool _isLoading = false;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFF0A0A0A),
      appBar: AppBar(
        backgroundColor: const Color(0xFF0A0A0A),
        foregroundColor: Colors.white,
        title: const Text('Bilgilerini Gir'),
        elevation: 0,
      ),
      body: _isLoading
          ? const Center(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  CircularProgressIndicator(color: Color(0xFF29B6F6)),
                  SizedBox(height: 16),
                  Text(
                    '🤖 AI programın hazırlanıyor...',
                    style: TextStyle(color: Colors.white70, fontSize: 16),
                  ),
                ],
              ),
            )
          : SingleChildScrollView(
              padding: const EdgeInsets.all(24),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  _buildTextField(_nameController, 'Adın', Icons.person),
                  const SizedBox(height: 16),
                  _buildTextField(_ageController, 'Yaş', Icons.cake, isNumber: true),
                  const SizedBox(height: 16),
                  _buildTextField(_weightController, 'Kilo (kg)', Icons.monitor_weight, isNumber: true),
                  const SizedBox(height: 16),
                  _buildTextField(_heightController, 'Boy (cm)', Icons.height, isNumber: true),
                  const SizedBox(height: 16),
                  _buildDropdown('Cinsiyet', _gender, ['Male', 'Female'],
    (v) => setState(() => _gender = v!),
    labels: {'Male': 'Erkek', 'Female': 'Kadın'}),
                  _buildDropdown('Aktivite seviyesi', _activityLevel,
                      ['Hareketsiz', 'Az aktif', 'Orta aktif', 'Çok aktif'],
                      (v) => setState(() => _activityLevel = v!)),
                  const SizedBox(height: 16),
                  _buildDropdown('Hedefin', _goal, ['Kilo ver', 'Formu koru', 'Kilo al'],
                      (v) => setState(() => _goal = v!)),
                  const SizedBox(height: 16),
                  _buildDropdown('Antrenman ortamı', _equipment,
                      ['Spor salonu', 'Ev (ekipmansız)', 'Ev (ekipmanlı)', 'Açık alan'],
                      (v) => setState(() => _equipment = v!)),
                  const SizedBox(height: 16),
                  _buildDropdown('Deneyim seviyesi', _experience.toString(),
                      ['1', '2', '3'],
                      (v) => setState(() => _experience = int.parse(v!)),
                      labels: {'1': 'Başlangıç', '2': 'Orta', '3': 'İleri'}),
                  const SizedBox(height: 16),
                  _buildSlider('Haftada kaç gün antrenman?', _frequency.toDouble(), 1, 7,
                      (v) => setState(() => _frequency = v.round()),
                      suffix: ' gün'),
                  const SizedBox(height: 16),
                  _buildSlider('Antrenman süresi (saat)', _sessionHours, 1, 3,
                      (v) => setState(() => _sessionHours = v),
                      divisions: 2, suffix: ' saat'),
                  const SizedBox(height: 16),
                  _buildTextField(_restrictionsController, 'Besin kısıtlamaları / alerjiler',
                      Icons.no_food, maxLines: 3,
                      hint: 'Örnek: gluten yiyemiyorum, vegan...'),
                  const SizedBox(height: 32),
                  SizedBox(
                    width: double.infinity,
                    height: 56,
                    child: ElevatedButton(
                      onPressed: _submit,
                      style: ElevatedButton.styleFrom(
                        backgroundColor: const Color(0xFF29B6F6),
                        foregroundColor: Colors.black,
                        shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(16),
                        ),
                      ),
                      child: const Text(
                        'Program Oluştur',
                        style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
                      ),
                    ),
                  ),
                  const SizedBox(height: 24),
                ],
              ),
            ),
    );
  }

  Widget _buildTextField(
    TextEditingController controller,
    String label,
    IconData icon, {
    bool isNumber = false,
    int maxLines = 1,
    String? hint,
  }) {
    return TextField(
      controller: controller,
      keyboardType: isNumber ? TextInputType.number : TextInputType.text,
      maxLines: maxLines,
      style: const TextStyle(color: Colors.white),
      decoration: InputDecoration(
        labelText: label,
        hintText: hint,
        hintStyle: TextStyle(color: Colors.white.withOpacity(0.3)),
        labelStyle: TextStyle(color: Colors.white.withOpacity(0.7)),
        prefixIcon: Icon(icon, color: const Color(0xFF29B6F6)),
        filled: true,
        fillColor: const Color(0xFF1A1A1A),
        border: OutlineInputBorder(
          borderRadius: BorderRadius.circular(12),
          borderSide: BorderSide.none,
        ),
        focusedBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(12),
          borderSide: const BorderSide(color: Color(0xFF29B6F6)),
        ),
      ),
    );
  }

  Widget _buildDropdown(
    String label,
    String value,
    List<String> items,
    void Function(String?) onChanged, {
    Map<String, String>? labels,
  }) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 4),
      decoration: BoxDecoration(
        color: const Color(0xFF1A1A1A),
        borderRadius: BorderRadius.circular(12),
      ),
      child: DropdownButtonFormField<String>(
        value: value,
        dropdownColor: const Color(0xFF1A1A1A),
        style: const TextStyle(color: Colors.white),
        decoration: InputDecoration(
          labelText: label,
          labelStyle: TextStyle(color: Colors.white.withOpacity(0.7)),
          border: InputBorder.none,
        ),
        items: items.map((item) {
          return DropdownMenuItem(
            value: item,
            child: Text(labels?[item] ?? item, style: const TextStyle(color: Colors.white)),
          );
        }).toList(),
        onChanged: onChanged,
      ),
    );
  }

  Widget _buildSlider(
    String label,
    double value,
    double min,
    double max,
    void Function(double) onChanged, {
    int? divisions,
    String suffix = '',
  }) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          '$label: ${value.round()}$suffix',
          style: TextStyle(color: Colors.white.withOpacity(0.7), fontSize: 14),
        ),
        Slider(
          value: value,
          min: min,
          max: max,
          divisions: divisions ?? (max - min).round(),
          activeColor: const Color(0xFF29B6F6),
          inactiveColor: Colors.white12,
          onChanged: onChanged,
        ),
      ],
    );
  }

  Future<void> _submit() async {
    if (_ageController.text.isEmpty ||
        _weightController.text.isEmpty ||
        _heightController.text.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Lütfen yaş, kilo ve boyu girin.')),
      );
      return;
    }

    setState(() => _isLoading = true);

    try {
      final result = await ApiService.generateProgram(
        name: _nameController.text,
        age: int.parse(_ageController.text),
        gender: _gender,
        weight: double.parse(_weightController.text),
        height: double.parse(_heightController.text),
        activityLevel: _activityLevel,
        goal: _goal,
        frequency: _frequency,
        experience: _experience,
        sessionHours: _sessionHours,
        equipment: _equipment,
        restrictions: _restrictionsController.text,
      );

      if (mounted) {
        Navigator.push(
          context,
          MaterialPageRoute(builder: (_) => ResultScreen(data: result)),
        );
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Hata: $e')),
        );
      }
    } finally {
      if (mounted) setState(() => _isLoading = false);
    }
  }
}
