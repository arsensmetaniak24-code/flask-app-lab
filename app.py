from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
@app.route('/resume')
def resume():

    education = [
        {
            "degree" : "Bechelor's degree in Software Engineering",
            "place" : "Vasyl Stefanyk Carpathian National University",
            "year" : "2024-2028"
        },
        {
            "degree" : "High School Diploma",
            "place" : "Lyceum \"Intellect\"",
            "year" : "2020-2024"
        }
    ]
    skills = ["Problem-solving", "Teamwork", "Communication", "Adaptability", "Creativity"]
    technologies = ["Godot", "GDScript", "GDShader", "SQL", "Java", "Spring"]
    projects = [
        {
            "name" : "Our Squishy Hero",
            "description" : "A solo-developed 2d platformer game with 35 unique levels.",
            "link" : "https://arzzzen.itch.io/our-squishy-hero",
            "image" : "our_squishy_hero_image.png"
        },
        {
            "name" : "Our Perfect Spot",
            "description" : "A cute 2d puzzle about permutations.",
            "link" : "https://arzzzen.itch.io/our-perfect-spot",
            "image" : "our_perfect_spot_image.png"
        },
        {
            "name" : "AreaOfSight2D",
            "description" : "A godot plugin for calculating the area of sight.",
            "link" : "https://github.com/Arzzzen105/AreaOfSight2D",
            "image" : "area_of_sight_2d_image.png"
        }
    ]

    return render_template(
        'resume.html',
        title = "Resume",
        education=education,
        skills=skills,
        technologies=technologies,
        projects=projects,
        avatar='images/icon.png')

@app.route('/contacts')
def contacts():
    return render_template('contacts.html', title = "Contacts")

if __name__ == '__main__':
    app.run(debug=True)
