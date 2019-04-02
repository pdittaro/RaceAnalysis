import pdfkit


def main():
    print('Race result')
    pdfkit.from_url(
        'https://www.rvyc.bc.ca/RacingApps/Results/html/1548551990.htm', 'out.pdf')


if __name__ == "__main__":
    main()
