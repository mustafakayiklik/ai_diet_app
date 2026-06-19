import 'dart:convert';
import 'package:http/http.dart' as http;

class ApiService {
  static const String baseUrl = 'http://127.0.0.1:8000';

  static Future<Map<String, dynamic>> generateProgram({
    required String name,
    required int age,
    required String gender,
    required double weight,
    required double height,
    required String activityLevel,
    required String goal,
    required int frequency,
    required int experience,
    required double sessionHours,
    required String equipment,
    required String restrictions,
  }) async {
    final response = await http.post(
      Uri.parse('$baseUrl/generate-program'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'name': name,
        'age': age,
        'gender': gender,
        'weight': weight,
        'height': height,
        'activity_level': activityLevel,
        'goal': goal,
        'frequency': frequency,
        'experience': experience,
        'session_hours': sessionHours,
        'equipment': equipment,
        'restrictions': restrictions,
      }),
    );

    if (response.statusCode == 200) {
      return jsonDecode(utf8.decode(response.bodyBytes));
    } else {
      throw Exception('API hatası: ${response.statusCode}');
    }
  }

  static Future<String> chat(
    List<Map<String, String>> messages,
    Map<String, dynamic> profile,
  ) async {
    final response = await http.post(
      Uri.parse('$baseUrl/chat'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'messages': messages,
        'profile': profile,
      }),
    );

    if (response.statusCode == 200) {
      final data = jsonDecode(utf8.decode(response.bodyBytes));
      return data['reply'];
    } else {
      throw Exception('API hatası: ${response.statusCode}');
    }
  }
}
