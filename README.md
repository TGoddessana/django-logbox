<a name="readme-top"></a>

<div align="center">

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]

</div>


<!-- PROJECT LOGO -->
<br />
<div align="center">

  <a href="https://github.com/tgoddessana/Django-Logbox">
    <img src="https://raw.githubusercontent.com/TGoddessana/django-logbox/refs/heads/main/docs/img/django-logbox-logo.png"
style="width:200px;">
  </a>

<h3 align="center">Django-Logbox</h3>

  <p align="center">
    Your small, but useful django log box. 📦
    <br />
    <a href="https://tgoddessana.github.io/django-logbox/"><strong>Explore the docs »</strong></a>
    <br />
  </p>
</div>


<!---------------------------------------------------------------------------------------------->

<br/>

## Django-Logbox

`django-logbox` is a Django app that logs all `HttpRequest` information performed in `Django`.
The following information is recorded and can be viewed in the `Django Admin`:

- `http method`
- `request path`
- `http status code`
- `user-agent` string
- device, os, browser information (parsed from `user-agent`)
- `querystring`, `request body` information
- log creation time
- exception information (type, message, traceback)
- server IP, client IP
- request user, which can be `AnonymousUser` or `User` object

<br/>

### Example Screenshot

this is an example screenshot of the `Django Logbox` admin interface, showing logged requests and their details.

<img src="https://raw.githubusercontent.com/TGoddessana/django-logbox/refs/heads/main/docs/img/example-admin.png" alt="Django Logbox Admin Example" style="width: 100%; max-width: 800px;">

... you can also check the traceback of the exception if it exists, and the request body and querystring information in
detail page.

<img src="https://raw.githubusercontent.com/TGoddessana/django-logbox/refs/heads/main/docs/img/example-admin2.png" alt="Django Logbox Admin Example2" style="width: 100%; max-width: 800px;">

## License

---

Distributed under the MIT License. See `LICENSE` for more information.



<!---------------------------------------------------------------------------------------------->

<br/>

## Contact

---

- Author Email: twicegoddessana1229@gmail.com
- Project Link: [https://github.com/tgoddessana/Django-Logbox](https://github.com/tgoddessana/Django-Logbox)

<!---------------------------------------------------------------------------------------------->
<!---------------------------------------------------------------------------------------------->

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->

[contributors-shield]: https://img.shields.io/github/contributors/tgoddessana/Django-Logbox.svg?style=for-the-badge

[contributors-url]: https://github.com/tgoddessana/Django-Logbox/graphs/contributors

[forks-shield]: https://img.shields.io/github/forks/tgoddessana/Django-Logbox.svg?style=for-the-badge

[forks-url]: https://github.com/tgoddessana/Django-Logbox/network/members

[stars-shield]: https://img.shields.io/github/stars/tgoddessana/Django-Logbox.svg?style=for-the-badge

[stars-url]: https://github.com/tgoddessana/Django-Logbox/stargazers

[issues-shield]: https://img.shields.io/github/issues/tgoddessana/Django-Logbox.svg?style=for-the-badge

[issues-url]: https://github.com/tgoddessana/Django-Logbox/issues

[license-shield]: https://img.shields.io/github/license/tgoddessana/Django-Logbox.svg?style=for-the-badge

[license-url]: https://github.com/tgoddessana/Django-Logbox/blob/master/LICENSE.txt

[Python]: https://img.shields.io/badge/python-306998?style=for-the-badge&logo=python&logoColor=white


