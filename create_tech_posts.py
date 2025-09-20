import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'likhoncombd.settings')
django.setup()

from django.contrib.auth.models import User
from blog.models import Post, Tag

# Get the author
try:
    author = User.objects.get(username='Gemini')
except User.DoesNotExist:
    print("User 'Gemini' not found. Please create the user first.")
    exit()

# Create tags if they don't exist
tag_names = ['AI', 'Quantum Computing', 'Cybersecurity', 'Software Development', 'Cloud', 'Hardware']
tags = {}
for name in tag_names:
    tag, created = Tag.objects.get_or_create(name=name)
    tags[name] = tag

# Define the posts to be created
posts_to_create = [
    {
        'title': 'The Quantum Leap: Are We on the Brink of a Computing Revolution?',
        'content': """
        <p>Quantum computing has long been the stuff of science fiction, but recent breakthroughs suggest it might be closer to reality than we think. Companies like Google and IBM are making significant strides in developing stable quantum processors, known as qubits. While we're still years away from quantum laptops, the implications for fields like medicine, materials science, and cryptography are staggering.</p>
        <p>One of the most promising applications is in drug discovery. Simulating molecular interactions is a task that even the most powerful supercomputers struggle with. Quantum computers, however, could model these interactions with unprecedented accuracy, potentially leading to the rapid development of new life-saving drugs. The race is on, and the world is watching.</p>
        """,
        'tags': [tags['Quantum Computing'], tags['AI']]
    },
    {
        'title': 'Generative AI and the Future of Software Development',
        'content': """
        <p>The rise of large language models (LLMs) and generative AI is fundamentally changing the landscape of software development. Tools that can write code, suggest bug fixes, and even generate entire applications from a simple text prompt are becoming increasingly common. Is this the end of the road for human developers?</p>
        <p>Not quite. While AI can automate many of the more tedious aspects of coding, the need for skilled engineers to design, architect, and oversee complex systems is more critical than ever. The future, it seems, is one of collaboration, where developers leverage AI as a powerful assistant to build better software, faster.</p>
        """,
        'tags': [tags['AI'], tags['Software Development']]
    },
    {
        'title': 'The Zero-Day Threat: A New Era of Cybersecurity Challenges',
        'content': """
        <p>Cybersecurity experts are warning of a significant increase in "zero-day" vulnerabilities—flaws in software that are discovered and exploited by attackers before the vendor has a chance to release a patch. These attacks are notoriously difficult to defend against and can have devastating consequences.</p>
        <p>As our world becomes more interconnected, the attack surface for malicious actors expands. Experts are urging organizations to adopt a more proactive security posture, focusing on threat intelligence, continuous monitoring, and rapid incident response to mitigate the risks posed by these sophisticated threats.</p>
        """,
        'tags': [tags['Cybersecurity']]
    },
    {
        'title': 'Multi-Cloud is the New Standard: Navigating a Complex Ecosystem',
        'content': """
        <p>The days of relying on a single cloud provider are over. A multi-cloud strategy, which involves using services from two or more different public clouds, is now the de facto standard for modern enterprises. This approach offers greater flexibility, avoids vendor lock-in, and can improve resilience.</p>
        <p>However, managing a multi-cloud environment comes with its own set of challenges, including increased complexity, security concerns, and the need for specialized skills. Companies are turning to cloud management platforms and FinOps practices to optimize costs and streamline operations across their diverse cloud portfolios.</p>
        """,
        'tags': [tags['Cloud'], tags['Software Development']]
    },
    {
        'title': 'Neural Interfaces: The Next Frontier in Human-Computer Interaction?',
        'content': """
        <p>Imagine controlling your computer with just your thoughts. This is the promise of brain-computer interfaces (BCIs), a field that is rapidly advancing thanks to progress in neuroscience and machine learning. Companies are developing non-invasive neural interfaces that can translate brain signals into commands for external devices.</p>
        <p>While the initial applications are focused on helping people with paralysis and other medical conditions, the long-term vision is to create a seamless link between the human mind and the digital world. The ethical and societal implications are profound, and it's a conversation we need to start having now.</p>
        """,
        'tags': [tags['AI'], tags['Hardware']]
    }
]

# Create the posts
for post_data in posts_to_create:
    title = post_data['title']
    if not Post.objects.filter(title=title).exists():
        post = Post.objects.create(
            title=title,
            content=post_data['content'],
            author=author,
        )
        post.tags.set(post_data['tags'])
        print(f"Post '{title}' created successfully.")
    else:
        print(f"Post '{title}' already exists.")
