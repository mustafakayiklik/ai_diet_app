import 'package:flutter/material.dart';
import 'chat_screen.dart';

class ResultScreen extends StatefulWidget {
  final Map<String, dynamic> data;
  const ResultScreen({super.key, required this.data});

  @override
  State<ResultScreen> createState() => _ResultScreenState();
}

class _ResultScreenState extends State<ResultScreen> {
  int _selectedTab = 0;

  @override
  Widget build(BuildContext context) {
    final data = widget.data;
    final bmi = data['bmi']?.toString() ?? '-';
    final bmiCategory = data['bmi_category'] ?? '-';
    final tdee = data['tdee']?.toString() ?? '-';
    final calorieTarget = data['calorie_target']?.toString() ?? '-';
    final goal = data['goal'] ?? '-';
    final predictedWorkout = data['predicted_workout'] ?? '-';
    final predictedCalories = data['predicted_calories']?.toString() ?? '-';
    final aiDiet = data['ai_diet'] ?? '';
    final aiExercise = data['ai_exercise'] ?? '';
    final profile = data['profile'] ?? {};

    return Scaffold(
      backgroundColor: const Color(0xFF0A0A0A),
      appBar: AppBar(
        backgroundColor: const Color(0xFF0A0A0A),
        foregroundColor: Colors.white,
        title: Text(
          profile['name'] != null && profile['name'].toString().isNotEmpty
              ? 'Merhaba ${profile['name']}! 👋'
              : 'Programın Hazır! 👋',
        ),
        elevation: 0,
        actions: [
          IconButton(
            icon: const Icon(Icons.chat_bubble_outline, color: Color(0xFF29B6F6)),
            onPressed: () {
              Navigator.push(
                context,
                MaterialPageRoute(builder: (_) => ChatScreen(profile: profile)),
              );
            },
          ),
        ],
      ),
      body: Column(
        children: [
          Padding(
            padding: const EdgeInsets.all(16),
            child: Row(
              children: [
                _StatCard('BMI', '$bmi\n$bmiCategory'),
                const SizedBox(width: 8),
                _StatCard('Kalori İhtiyacı', '$tdee kcal'),
                const SizedBox(width: 8),
                _StatCard('Hedef', '$calorieTarget kcal'),
              ],
            ),
          ),
          Padding(
            padding: const EdgeInsets.symmetric(horizontal: 16),
            child: Row(
              children: [
                _StatCard('ML: Antrenman', predictedWorkout.isNotEmpty ? predictedWorkout : 'Cardio'),
                const SizedBox(width: 8),
                _StatCard('ML: Yakım', predictedCalories.isNotEmpty ? '$predictedCalories kcal' : '-'),
              ],
            ),
          ),
          const SizedBox(height: 16),
          Row(
            children: [
              _TabButton('Diyet', 0, _selectedTab, (i) => setState(() => _selectedTab = i)),
              _TabButton('Egzersiz', 1, _selectedTab, (i) => setState(() => _selectedTab = i)),
            ],
          ),
          Expanded(
            child: SingleChildScrollView(
              padding: const EdgeInsets.all(16),
              child: Container(
                padding: const EdgeInsets.all(16),
                decoration: BoxDecoration(
                  color: const Color(0xFF1A1A1A),
                  borderRadius: BorderRadius.circular(12),
                ),
                child: Text(
                  _selectedTab == 0 ? aiDiet : aiExercise,
                  style: const TextStyle(color: Colors.white70, fontSize: 14, height: 1.6),
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }
}

class _StatCard extends StatelessWidget {
  final String title;
  final String value;
  const _StatCard(this.title, this.value);

  @override
  Widget build(BuildContext context) {
    return Expanded(
      child: Container(
        padding: const EdgeInsets.all(12),
        decoration: BoxDecoration(
          color: const Color(0xFF1A1A1A),
          borderRadius: BorderRadius.circular(12),
          border: Border.all(color: Colors.white.withOpacity(0.08)),
        ),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(title, style: TextStyle(color: Colors.white.withOpacity(0.5), fontSize: 11)),
            const SizedBox(height: 4),
            Text(value, style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold, fontSize: 13)),
          ],
        ),
      ),
    );
  }
}

class _TabButton extends StatelessWidget {
  final String label;
  final int index;
  final int selected;
  final void Function(int) onTap;
  const _TabButton(this.label, this.index, this.selected, this.onTap);

  @override
  Widget build(BuildContext context) {
    final isSelected = index == selected;
    return Expanded(
      child: GestureDetector(
        onTap: () => onTap(index),
        child: Container(
          padding: const EdgeInsets.symmetric(vertical: 12),
          decoration: BoxDecoration(
            border: Border(
              bottom: BorderSide(
                color: isSelected ? const Color(0xFF29B6F6) : Colors.transparent,
                width: 2,
              ),
            ),
          ),
          child: Text(
            label,
            textAlign: TextAlign.center,
            style: TextStyle(
              color: isSelected ? const Color(0xFF29B6F6) : Colors.white38,
              fontWeight: isSelected ? FontWeight.bold : FontWeight.normal,
            ),
          ),
        ),
      ),
    );
  }
}
