from imdb import Cinemagoer

# Búa til tilvik af Cinemagoer klasanum
ia = Cinemagoer()

# Sækja upplýsingar um Kate Winslet með því að nota persónu ID
# Kate Winslet hefur ID númerið '0000701' á IMDb
kate_winslet = ia.get_person('0000701')

# Prenta nafn hennar og aðrar tiltækar upplýsingar
print("Name:", kate_winslet['name'])

# Prófa að prenta út upplýsingar um fæðingardag og fæðingarstað
print("Date of Birth:", kate_winslet.get('birth date', 'Date of Birth not available'))
print("Place of Birth:", kate_winslet.get('birth info', 'Place of Birth not available'))

# Sýna kvikmyndir sem hún er þekkt fyrir
print("Known for Movies:", [movie['title'] for movie in kate_winslet.get('filmography', {}).get('actress', [])[:5]])

# Birta öll aðgengileg lykilorð fyrir upplýsingar um hana
print("All available keys:", kate_winslet.keys())

# Uppfæra með 'main' upplýsingasettinu
ia.update(kate_winslet, info=['main'])

# Athuga hvort 'mini biography' upplýsingarnar eru til og prenta þær ef svo er
if 'mini biography' in kate_winslet:
    print("Mini Biography:", kate_winslet['mini biography'])
else:
    print("No biography available for Kate Winslet.")

# Sýna annað trivia ef það er tiltækt
if 'trivia' in kate_winslet:
    print("Trivia about Kate Winslet:")
    for fact in kate_winslet['Trivia'][:5]:  # Prenta fyrstu 5 trivia atriðin til að forðast of mikið magn
        print("-", fact)
else:
    print("No trivia available for Kate Winslet.")