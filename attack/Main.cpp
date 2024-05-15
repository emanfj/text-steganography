#include <fstream>
#include <iostream>
#include <string>
#include <format>
#include <deque>

int main() {
	const unsigned char special_byte_1 = 0xe2;
	const unsigned char special_byte_2 = 0x80;
	const unsigned char special_byte_3v1 = 0x8c;
	const unsigned char special_byte_3v2 = 0x8d;

	std::ifstream f("steg_text.txt");
	bool isCypheringBit = false;
	std::deque<unsigned char> buffer = { 0,0 };

	std::string msgBinary = "";
	while (f) {
		char c;
		f.get(c);
		buffer.push_back(c);

		std::string binary = std::format("{:0>8b}", buffer[2]);
		std::string hex = std::format("{:x}", buffer[2]);

		std::cout << "Char: " << c << '\t' << "bits: " << binary << '\t' << "hex: " << hex;

		if (buffer[2] == special_byte_1 || buffer[2] == special_byte_2 ||
			buffer[2] == special_byte_3v1 || buffer[2] == special_byte_3v2)
		{
			std::cout << "\t*";
		}

		if (buffer[0] == special_byte_1 && buffer[1] == special_byte_2 &&
			(buffer[2] != special_byte_3v1 || buffer[2] != special_byte_3v2))
		{
			msgBinary += (buffer[2] & 1) ? '1' : '0';
		}

		std::cout << '\n';
		buffer.pop_front();
	}

	std::cout << "\n\nHidden message in binary:\n" << msgBinary << '\n';

	std::cout << "Converted to ASCII: ";
	for (int i = 0; i < msgBinary.size(); i += 8) {
		std::string byte = msgBinary.substr(i, 8);
		int byte_int = std::stoi(byte, nullptr, 2);

		std::cout << (char)byte_int;
	}

	return 0;
}