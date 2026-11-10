from flask import render_template, redirect, url_for, flash, request
from . import app, logger
from .forms import ContactForm

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

@app.route('/contacts', methods=['GET', 'POST'])
def contacts():

    form = ContactForm()

    if form.validate_on_submit():
        try:
            logger.info(f"Received message from {form.name.data} ({form.email.data}, {form.phone.data}). Subject: '{form.subject.data}'. Message: '{form.message.data}'")
        except Exception as e:
            flash(f"Error while logging message! Try later", "danger")
            return render_template('contacts.html', title="Contacts", form=form)
        flash('Your message has been sent!', 'success')
        return redirect(url_for('contacts'))

    if request.method == 'POST':
        flash("Invalid form submission! Check your input again", "warning")

    return render_template('contacts.html', title="Contacts", form=form)
